import pyzabbix
import zm.utils
import zm.zutils

@zm.utils.login
def list(conn):
    # FIXME didn't find a way to distinguish between hostids that refer
    # to templateid or indeed to hostid
    l = []
    for macro in conn.usermacro.get(globalmacroids="extend", output="extend"):
        if zm.zutils.get(conn, type="host", parameter="hostid", value=macro["hostid"], output=["hostid"]):
            scope = "Host level"
        elif zm.zutils.get(conn, type="template", parameter="hostid", value=macro["hostid"], output=["templateid"]):
            scope = "Template level"
        else:
            raise NotImplementedError("ID '%s' not matched neither as template or host")
        l.append([scope, macro["hostmacroid"], macro["macro"], macro["value"]])
    zm.utils.print_table(["Scope", "ID", "Name", "Value"], sorted(l))


@zm.utils.login
def update(conn, id, value):
    try:
        conn.usermacro.update(hostmacroid=id, value=value)
        #logging.debug("User macro ID %s successfully updated. New value: %s" % (id, value))
    except pyzabbix.ZabbixAPIException, e:
        #logger.debug(e)
        raise pyzabbix.ZabbixAPIException(e)
