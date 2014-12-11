===============================
zabbix-cli-ent
===============================

Zabbix management command-line client

* Free software: Apache license
* Source: https://github.com/orviz/zabbix-cli-ent
* Bugs: https://github.com/orviz/zabbix-cli-ent/issues


zabbix-cli-ent allows to perform actions on a Zabbix server
through command line.

Zabbix web interface usually is the most suitable way for
administration tasks, however there are times when you
need to modify settings non-interactively (scripts, ..) or
even certain actions easily done by command line.


Getting Started
---------------

Install `zabbix-cli-ent` using `pip`, either by getting the
version uploaded in PyPi:

.. code:: bash

    $ pip install zm

or the one from the current repo:

.. code:: bash

    $ git clone https://github.com/orviz/zabbix-cli-ent.git
    $ cd zabbix-cli-ent && pip install .


Basic Usage
-----------

.. code:: bash

    $ zm --help

will list the current actions that can be performed.

Depending on the subcommand it will have different options;
rely on the `--help` option to learn about each one.


**NOTE**: You can provide the connection details as options or
via a configuration file. Either way, the login, password
and url must be provided in order to get a successfully
connection.

Use it programatically
----------------------

You can also use zabbix-cli-ent as a Python library to get data
from a Zabbix API.

For that you first need to provide the credentials to be able to
access any of the available functionality. As an example:

.. code:: Python

    import zm.trigger
    from oslo.config import cfg

    CONF = cfg.CONF
    CONF.username="foo"
    CONF.password="bar"
    CONF.url="https://example.com/zabbix"


    print zm.trigger.list(host="host.example.com",
                          priority="DISASTER",
                          omit_ack=True,)

Extending Functionality
-----------------------

The code allows to easily extend the functionality. To do
so:

1. Create a new ``Command`` inherited class that will
   handle the new functionality.

   - ``__init__()``, where you will define the new action's options.
   - ``run()``, sets the work to be done.

2. Add the brand new class to: ``commands.py`` > ``add_command_parsers()``

There you go!
