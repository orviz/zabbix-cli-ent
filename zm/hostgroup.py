from __future__ import print_function

import zm.utils
import zm.zutils


@zm.utils.login
def list(conn):
    zm.utils.print_table(["ID", "Name"],
                         [[i["groupid"],i["name"]]
                         for i in zm.zutils.get(conn,
                                                type="hostgroup",
                                                output=["groupid", "name"])])
