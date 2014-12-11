import pyzabbix
import zm.utils
import zm.zutils


@zm.utils.login
def list(conn):
    # FIXME didn't find a way to distinguish between hostids that refer
    # to templateid or indeed to hostid
    l = []
    for macro in zm.zutils.get(conn,
                               type="usermacro",
                               output="extend",
                               **{"globalmacroids": "extend"}):
        # Set scope
        if zm.zutils.get(conn,
                         type="host",
                         params={"hostid": macro["hostid"]},
                         output=["hostid"]):
            scope = "Host level"
            macro.update({"scope": "Host level"})
        elif zm.zutils.get(conn,
                           type="template",
                           params={"hostid": macro["hostid"]},
                           output=["templateid"]):
            scope = "Template level"
            macro.update({"scope": "Template level"})
        else:
            raise NotImplementedError("ID '%s' not matched neither as template or host")

        l.append(macro)

    return l


@zm.utils.login
def update(conn, id, value):
    try:
        conn.usermacro.update(hostmacroid=id,
                              value=value)
        #logging.debug("User macro ID %s successfully updated. New value: %s" % (id, value))
    except pyzabbix.ZabbixAPIException, e:
        #logger.debug(e)
        raise pyzabbix.ZabbixAPIException(e)
