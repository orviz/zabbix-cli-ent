import pyzabbix
import zm.utils
import zm.zutils

@zm.utils.login
def list(conn, host=None, group=None):
    l = []
    columns = ["", "Template Name"]
    if host:
        columns = ["Host", "Template Name"]
        for host in host:
            try:
                l.append((host, zm.zutils.get(conn, 
                                              type="host",
                                              parameter="name",
                                              value=host,
                                              selectParentTemplates="extend")[0]["parentTemplates"]))
            except IndexError:
                pass
                #logging.error("Host not found: %s" % host)
    elif group:
        columns = ["Hostgroup", "Template Name"]
        for group in group:
            try:
                l.append((group, zm.zutils.get(conn,
                                               type="hostgroup",
                                               parameter="name",
                                               value=group,
                                               selectTemplates="extend")[0]["templates"]))
            except IndexError:
                pass
                #logging.error("Hostgroup not found: %s" % group)
    else:
        l.append((None, zm.zutils.get(conn,
                                      type="template",
                                      parameter=None,
                                      value=None,
                                      output=["name"])))

    row_content = [[host, [d["name"] for d in data]] for host, data in l]
    zm.utils.print_table(columns, row_content)

