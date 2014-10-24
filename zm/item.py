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
    try:
        int(host)
        parameter = "hostids"
    except ValueError:
        parameter = "host"

    l = []
    for item in zm.zutils.get(conn,
                        type="item",
                        parameter=parameter,
                        value=host,
                        output=["status", "name"]):
        l.append([item["itemid"], item["name"], ITEM_STATUS[item["status"]]])
    if l:
        zm.utils.print_table(["ID", "Name", "Value"], sorted(l))

@zm.utils.login
def update(conn, id, status):
    try:
        conn.item.update(itemid=id, status=str(status))
        print("Item %s %s" % (id, ITEM_STATUS[str(status)].lower()))
    except pyzabbix.ZabbixAPIException, e:
        if e.args[1] == -32602:
            print("Permission denied: failed to enable item.", file=sys.stderr)
