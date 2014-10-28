
def get(conn, type, parameter=None, value=None, output="extend", **kwargs):
    types = {
        "host": conn.host.get,
        "hostgroup": conn.hostgroup.get,
        "item": conn.item.get,
        "template": conn.template.get,
    }
    if parameter:
        return types[type](filter={parameter: value}, output=output, **kwargs)
    else:
        return types[type](output=output, **kwargs)


