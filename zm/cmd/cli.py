import sys
import zm.commands
import zm.config

from oslo.config import cfg


opts = [
    cfg.StrOpt("username",
               help="Zabbix login."),
    cfg.StrOpt("password",
               help="Zabbix credentials."),
    cfg.StrOpt("url",
               help="Zabbix endpoint."),
]


CONF = cfg.CONF
CONF.register_cli_opts(opts)


def main():
    zm.config.parse_args(sys.argv)
    zm.commands.CommandManager().execute()


if __name__ == "__main__":
    main()
