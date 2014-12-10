from __future__ import print_function

import prettytable
import pyzabbix
import requests
import sys

from oslo.config import cfg

CONF = cfg.CONF


def login(func):
    def _login(*args, **kwargs):
        try:
            s = requests.Session()
            s.auth = (CONF.username,
                      CONF.password)
            s.verify = False

            conn = pyzabbix.ZabbixAPI(CONF.url, s)
            #logger.debug("Login to Zabbix (user '%s')" % CONF.username)
            print("Login to Zabbix (user '%s')" % CONF.username)
            conn.login(CONF.username, CONF.password)
        except requests.exceptions.HTTPError:
            #logger.error("Zabbix authorization failed")
            print("Zabbix authorization failed")
            sys.exit(1)

        #logger.debug("Successfully connected to Zabbix API v%s" % conn.api_version())
        return func(conn, *args, **kwargs)
    return _login


class TableOutput(object):
    def __init__(self, l, output):
        self.l = l
        self.output = output

    def __str__(self):
        l = []
        for d in self.l:
            l.append([d[i] for i in self.output.keys()])

        return self.print_table(self.output.values(), sorted(l))

    def print_table(self, columns, row_content, padding_width=1):
        """
        Prints a prettytable for the arguments received.
            columns; list of column names
            row_content; list of lists containing column values
        """
        x = prettytable.PrettyTable(columns)
        x.padding_width = padding_width
        for row in row_content:
            x.add_row(row)
        return str(x)
