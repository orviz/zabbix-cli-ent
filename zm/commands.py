from __future__ import print_function

import sys
import zm.exception
import zm.hostgroup
import zm.item
import zm.macro
import zm.template
import zm.trigger
import zm.utils

from oslo.config import cfg
from zm.utils import TableOutput


CONF = cfg.CONF


def add_command_parsers(subparsers):
    CommandHostgroupList(subparsers)
    CommandItemList(subparsers)
    CommandItemEnable(subparsers)
    CommandItemDisable(subparsers)
    CommandMacroList(subparsers)
    CommandMacroUpdate(subparsers)
    CommandTemplateList(subparsers)
    CommandTriggerList(subparsers)


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

        self.output = {"groupid": "ID", "name": "Name"}

    def run(self):
        print(TableOutput(zm.hostgroup.list(),
                          output=self.output))


class CommandItemList(Command):
    def __init__(self, parser, name="item-list",
                 cmd_help="List host items."):
        super(CommandItemList, self).__init__(parser, name, cmd_help)

        self.parser.add_argument("host",
                                 metavar="ID/HOSTNAME",
                                 help="Zabbix hostname or ID.")

        self.output = {"itemid": "ID", "name": "Name", "status": "Value" }

    def run(self):
        print(TableOutput(zm.item.list(CONF.command.host),
                          output=self.output))


class CommandItemEnable(Command):
    def __init__(self, parser, name="item-enable",
                 cmd_help="Enable host items."):
        super(CommandItemEnable, self).__init__(parser, name, cmd_help)

        self.parser.add_argument("id",
                                 nargs="+",
                                 metavar="ID/NAME",
                                 help="Zabbix item name or ID.")

        self.parser.add_argument("--host",
                                 metavar="ID/HOSTNAME",
                                 help="Filter by Zabbix hostname or ID.")

        self.parser.add_argument("--hostgroup",
                                 metavar="ID/HOSTGROUP",
                                 help="Filter by Zabbix hostgroup name or ID.")

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
                                 nargs="+",
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

        self.output = {"scope": "Scope",
                       "hostmacroid": "ID",
                       "macro": "Name",
                       "value": "Value"}

    def run(self):
        print(TableOutput(zm.macro.list(),
                          output=self.output))


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
                                 help="Zabbix host name.")

        self.parser.add_argument("--group",
                                 metavar="HOSTGROUP",
                                 help="Zabbix hosgroup name.")

        self.output = {"templateid": "ID",
                       "name": "Name",
                       "status": "Status"}

    def run(self):
        print(TableOutput(zm.template.list(CONF.command.host,
                                           CONF.command.group),
                          output=self.output))


class CommandTriggerList(Command):
    def __init__(self, parser, name="trigger-list",
                 cmd_help="List host triggers."):
        super(CommandTriggerList, self).__init__(parser, name, cmd_help)

        self.parser.add_argument("--host",
                                 metavar="ID/HOSTNAME",
                                 help="Zabbix hostname or ID.")

        self.parser.add_argument("--priority",
                                 "-p",
                                 metavar="[DISASTER|HIGH|AVERAGE|WARNING|INFORMATION|NOTCLASSIFIED]",
                                 help="Trigger priority or ID.")

        self.parser.add_argument("--last-change-since",
                                 metavar="UNIX TIMESTAMP",
                                 help="(epoch) time from which triggers have changed their state.")

        self.parser.add_argument("--problematic",
                                 action="store_true",
                                 help="Show only triggers in a problem state.")

        self.parser.add_argument("--monitored",
                                 action="store_true",
                                 help="Show only triggers mapped to enabled items.")

        self.parser.add_argument("--unacknowledged",
                                 action="store_true",
                                 help="Show only unacknowledged triggers.")

        self.output = {"triggerid": "ID",
                       "description": "Description",
                       "host_at": "Host name",
                       "value": "Status",
                       "priority": "Priority"}

    def run(self):
        if CONF.command.last_change_since:
            self.output.update({"lastchange": "Last change"})

        print(TableOutput(zm.trigger.list(CONF.command.host,
                                          priority=CONF.command.priority,
                                          last_change_since=CONF.command.last_change_since,
                                          problematic=CONF.command.problematic,
                                          monitored=CONF.command.monitored,
                                          unacknowledged=CONF.command.unacknowledged),
                          self.output))


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
