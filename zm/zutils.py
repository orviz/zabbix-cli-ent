
def get(conn, type, parameter, value, output="extend", **kwargs):
    types = {
        "template": conn.template.get,
        "host": conn.host.get,
        "hostgroup": conn.hostgroup.get,
    }
    if parameter:
        return types[type](filter={parameter: value}, output=output, **kwargs)
    else:
        return types[type](output=output, **kwargs)


