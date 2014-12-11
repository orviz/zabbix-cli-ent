from __future__ import print_function

import pyzabbix
import sys
import zm.utils
import zm.zutils


PRIORITY = {
    "NOTCLASSIFIED": "0",
    "INFORMATION": "1",
    "WARNING": "2",
    "AVERAGE": "3",
    "HIGH": "4",
    "DISASTER": "5",
}


@zm.utils.login
def list(conn,
         host=None,
         priority=None,
         last_change_since=None,
         problematic=True,
         monitored=True,
         unacknowledged=True):
    params = {}
    flags = {}

    flags["selectHosts"] = "extend"

    if host:
        try:
            int(host)
            params["hostids"] = host
        except ValueError:
            params["host"] = host

    if priority:
        try:
            params["priority"] = PRIORITY[priority]
        except IndexError:
            try:
                int(priority)
                params["priority"] = priority
            except ValueError:
                pass

    if problematic:
        params["value"] = "1"

    if last_change_since:
        flags["lastChangeSince"] = last_change_since

    if monitored:
        flags["monitored"] = "extend"

    if unacknowledged:
        flags["withLastEventUnacknowledged"] = "extend"


    l = []
    for trigger in zm.zutils.get(conn,
                                 type="trigger",
                                 params=params,
                                 # 'extend' is not recommended since
                                 # can hit memory allocation on server
                                 output=["triggerid",
                                         "description",
                                         "value",
                                         "hosts",
                                         "priority",
                                         "lastchange"],
                                 **flags):
        trigger.update({"host_at": trigger["hosts"][0]["host"]})
        l.append(trigger)

    return l
