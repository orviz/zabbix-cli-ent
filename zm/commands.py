import zm.exception
import zm.macro
import zm.utils

from oslo.config import cfg

CONF = cfg.CONF


def add_command_parsers(subparsers):
    CommandMacroList(subparsers)
    CommandMacroUpdate(subparsers)


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


class CommandManager(object):
    def execute(self):
        try:
            CONF.command.func()
        except zm.exception.ZMException as e:
            print >> sys.stderr, "ERROR: %s" % e
            sys.exit(1)
        except KeyboardInterrupt:
            print >> sys.stderr, "\nExiting..."
            sys.exit(0)
