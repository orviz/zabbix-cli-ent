from __future__ import print_function

import zm.utils
import zm.zutils


@zm.utils.login
def list(conn):
    return zm.zutils.get(conn,
                         type="hostgroup",
                         output="extend")
