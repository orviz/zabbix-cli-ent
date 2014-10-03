
def get(conn, type, parameter, value, output="extend"):
    types = {
        "template": conn.template.get,
        "host": conn.host.get,
    }
    return types[type](filter={parameter: value}, output=output)


