from __future__ import print_function

import sys
import zm.exception
import zm.hostgroup
import zm.item
import zm.macro
import zm.template
import zm.utils

from oslo.config import cfg


CONF = cfg.CONF


def add_command_parsers(subparsers):
    CommandHostgroupList(subparsers)
    CommandItemList(subparsers)
    CommandItemEnable(subparsers)
    CommandItemDisable(subparsers)
    CommandMacroList(subparsers)
    CommandMacroUpdate(subparsers)
    CommandTemplateList(subparsers)


command_opt = cfg.SubCommandOpt('command',
                                title='Commands',
                                help='Show available commands.',
                                handler=add_command_parsers)

CONF.register_cli_opt(command_opt)


class Command(object):
    def __init__(self, parser, name, cmd_help):
        self.name = name
        self.cmd_help = cmd_help
        self.parser = parser.add_parser(name, help=cmd_help)
        self.parser.set_defaults(func=self.run)

    def run(self):
        raise NotImplementedError("Method must me overriden on subclass")


class CommandHostgroupList(Command):
    def __init__(self, parser, name="hostgroup-list",
                 cmd_help="List hostgroups."):
        super(CommandHostgroupList, self).__init__(parser, name, cmd_help)

    def run(self):
        zm.hostgroup.list()


class CommandItemList(Command):
    def __init__(self, parser, name="item-list",
                 cmd_help="List host items."):
        super(CommandItemList, self).__init__(parser, name, cmd_help)

        self.parser.add_argument("host",
                                 metavar="ID/HOSTNAME",
                                 help="Zabbix hostname or ID.")

    def run(self):
        zm.item.list(CONF.command.host)


class CommandItemEnable(Command):
    def __init__(self, parser, name="item-enable",
                 cmd_help="Enable host items."):
        super(CommandItemEnable, self).__init__(parser, name, cmd_help)

        self.parser.add_argument("id",
                                 nargs="*",
                                 metavar="ID/NAME",
                                 help="Zabbix item name or ID.")

        self.parser.add_argument("--host",
                                 metavar="HOST",
                                 help="Filter by Zabbix host.")

        self.parser.add_argument("--hostgroup",
                                 metavar="HOSTGROUP",
                                 help="Filter by Zabbix hostgroup.")

    def run(self):
        zm.item.update(CONF.command.id,
                       0,
                       CONF.command.host,
                       CONF.command.hostgroup)


class CommandItemDisable(Command):
    def __init__(self, parser, name="item-disable",
                 cmd_help="Disable host items."):
        super(CommandItemDisable, self).__init__(parser, name, cmd_help)

        self.parser.add_argument("id",
                                 metavar="ID",
                                 help="Zabbix item name or ID.")

        self.parser.add_argument("--host",
                                 metavar="HOST",
                                 help="Filter by Zabbix host.")

        self.parser.add_argument("--hostgroup",
                                 metavar="HOSTGROUP",
                                 help="Filter by Zabbix hostgroup.")

    def run(self):
        zm.item.update(CONF.command.id,
                       1,
                       CONF.command.host,
                       CONF.command.hostgroup)


class CommandMacroList(Command):
    def __init__(self, parser, name="macro-list",
                 cmd_help="List user macros."):
        super(CommandMacroList, self).__init__(parser, name, cmd_help)

    def run(self):
        zm.macro.list()


class CommandMacroUpdate(Command):
    def __init__(self, parser, name="macro-update",
                 cmd_help="Update user macros."):
        super(CommandMacroUpdate, self).__init__(parser, name, cmd_help)

        self.parser.add_argument("id",
                                 metavar="ID",
                                 help="Zabbix macro ID.")

        self.parser.add_argument("value",
                                 metavar="VALUE",
                                 help="Zabbix value.")

    def run(self):
        zm.macro.update(CONF.command.id,
                        CONF.command.value)


class CommandTemplateList(Command):
    def __init__(self, parser, name="template-list",
                 cmd_help="List templates."):
        super(CommandTemplateList, self).__init__(parser, name, cmd_help)

        self.parser.add_argument("--host",
                                 metavar="HOST",
                                 nargs="*",
                                 help="Zabbix host name. Accepts multiple values.")

        self.parser.add_argument("--group",
                                 metavar="HOSTGROUP",
                                 nargs="*",
                                 help="Zabbix hosgroup name. Accepts multiple values.")

    def run(self):
        zm.template.list(CONF.command.host,
                         CONF.command.group)

class CommandManager(object):
    def execute(self):
        try:
            CONF.command.func()
        except zm.exception.ZMException as e:
            print("ERROR: %s" % e, file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print ("\nExiting...", sys.stderr)
            sys.exit(0)
