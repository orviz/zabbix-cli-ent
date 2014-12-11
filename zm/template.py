import pyzabbix
import zm.utils
import zm.zutils

@zm.utils.login
def list(conn, host=None, group=None):
    if host:
        return zm.zutils.get(conn,
                             type="host",
                             params={"name": host},
                             output="extend",
                             **{"selectParentTemplates": "extend"})[0]["parentTemplates"]
    elif group:
        return zm.zutils.get(conn,
                             type="hostgroup",
                             params={"name": group},
                             output="extend",
                             selectTemplates="extend")[0]["templates"]
    else:
        return zm.zutils.get(conn,
                             type="template",
                             output="extend")
