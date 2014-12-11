
def get(conn, type, params={}, output="extend", **kwargs):
    types = {
        "host": conn.host.get,
        "hostgroup": conn.hostgroup.get,
        "item": conn.item.get,
        "template": conn.template.get,
        "trigger": conn.trigger.get,
        "usermacro": conn.usermacro.get,
    }
    if params:
        return types[type](filter=params, output=output, **kwargs)
    else:
        return types[type](output=output, **kwargs)
