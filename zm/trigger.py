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
         host,
         priority=None,
         omit_ack=False):
    params = {}
    flags = {}

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

    if omit_ack:
        flags["withUnacknowledgedEvents"] = "extend"

    return zm.zutils.get(conn,
                         type="trigger",
                         params=params,
                         output="extend",
                         **flags)
