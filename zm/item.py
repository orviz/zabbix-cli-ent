from __future__ import print_function

import pyzabbix
import sys
import zm.utils
import zm.zutils


ITEM_STATUS = {
    "0": "Enabled",
    "1": "Disabled",
    "3": "Not supported",
}

@zm.utils.login
def list(conn, host):
    params = {}

    try:
        int(host)
        params["hostids"] = host
    except ValueError:
        params["host"] = host

    return zm.zutils.get(conn,
                         type="item",
                         params=params,
                         value=host,
                         output="extend")


@zm.utils.login
def update(conn, id, status, host=None, hostgroup=None):
    items = []
    for narg in id:
        try:
            int(narg)
            parameter = "itemid"
        except ValueError:
            parameter = "name"

        params = {parameter: narg}
        print(params)

        items.extend(zm.zutils.get(conn,
                                   type="item",
                                   params={parameter: narg},
                                   output=["status", "name"],
                                   **{"selectHosts": ["name"]}))

    h_parameter = None
    if host:
        try:
            int(host)
            h_parameter = "hostids"
        except ValueError:
            h_parameter = "host"
    hg_parameter = None
    if hostgroup:
        try:
            int(hostgroup)
            hg_parameter = "groupids"
        except ValueError:
            hg_parameter = "group"

    if host or hostgroup:
        hitems = zm.zutils.get(conn,
                              type="item",
                              output=["status", "name"],
                              **{"filter": {"name": id,
                                            h_parameter : host,
                                            hg_parameter: hostgroup},
                                 "selectHosts": ["name"]})

        l_items = [i["itemid"] for i in items]
        for hi in hitems:
            if not hi["itemid"] in l_items:
                items.append(hi)

    try:
        for item in items:
            conn.item.update(itemid=item["itemid"], status=str(status))
            print("Item <%s (%s)> %s on host %s" % (item["name"],
                                                    item["itemid"],
                                                    ITEM_STATUS[str(status)].lower(),
                                                    item["hosts"][0]["name"]))
        if not items:
            print("No matching item found")
    except pyzabbix.ZabbixAPIException, e:
        if e.args[1] == -32602:
            print("Permission denied: failed to enable item.", file=sys.stderr)


