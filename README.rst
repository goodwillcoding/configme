The GonfigMe Configuration Generation Framework and Utility
===========================================================

About
-----

ConfigMe is a small, fast, down-to-earth, open source configuration generation
framework and command line utility. It makes generation of real-world
configuration files and deployment more fun, more predictable, and more
productive.

ConfigMe is written in Python, uses Jinja2 for templates and INI files
for settings configuration. Support for Django, Mako and other templates is
planned.

What problem does ConfigMe solve for YOU!
-----------------------------------------

Whether used in production, staging or development the majority of the
configuration files are usually 95% identical and it can prove time consuming
and error-prone to maintain them in sync.

ConfigMe solves this for you by applying role's settings against the templates
containing the configuration and generates the configuration set you need.

:ref:`Thus tutorial<tutorial>` will show how to use ConfigMe.

Project Status
--------------

Project is still in development at 85% completion. That means it works but
there no guarantees it won't break. The names, command-line options and code
interfaces may change so backward compatibility is currently not guaranteed.

Test Coverage
~~~~~~~~~~~~~

**Current unit-test coverage stands at 91% using nose + nosexcover line
coverage tool.**


.. _installation:

Installation
------------

1. Clone the ConfigMe repo
2. Setup a virtualenv environment
3. python ./setup develop
4. Run `configme --help`


.. _tutorial:

Tutorial
--------

To demonstrate the use of of `ConfigMe` we will generate set of development and
production configuration for NginX for a project called `my-site`.

**First make sure ConfigMe is installed and you can run `configme` utility on
the command-line**. :ref:`Following the Installion instruction <installation>`
will help you.

Now lets look at a typical NginX configuration setup.

.. code-block :: console

    /etc
    |-- nginx.conf
    `-- sites-available
        `-- my-site.conf

In our example nginx.conf production configuration we want gzipping on while
development configuration will have it off.

Additionally we want my-site to be served on port 80 in production and port
8080 in development.


Configuration Folder Skeleton and Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First create the folder skeleton containing the files and a test output folder:

.. code-block :: console

    $ cd /tmp

    $ mkdir -p /tmp/configme/templates/etc/sites-available
    $ mkdir -p /tmp/configme/output
    $ mkdir -p /tmp/configme/settings

    $ touch /tmp/configme/templates/etc/nginx.conf
    $ touch /tmp/configme/templates/etc/sites-available/my-sites.conf

    $ touch /tmp/configme/settings/development.settings
    $ touch /tmp/configme/settings/production.settings


That should create you the following folders and files:

.. code-block :: console

    /tmp/configme/
    |-- output
    |-- settings
    |   |-- development.settings
    |   `-- production.settings
    `-- templates
        `-- etc
            |-- nginx.conf
            `-- sites-available
                `-- my-sites.conf


Edit **/tmp/configme/templates/etc/nginx.conf**

.. code-block :: nginx
   :linenos:
   :emphasize-lines: 22

    user www-data;
    worker_processes 4;
    pid /var/run/nginx.pid;

    events {
        worker_connections 768;
    }

    http {
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        gzip {{gzip_status}};
        include /etc/nginx/sites-enabled/*;
    }


The config file is a Jinja2 template and line 22 contains `gzip_status`
variable.

Edit **/tmp/configme/templates/etc/sites-available/my-sites.conf**

.. code-block :: nginx
   :linenos:
   :emphasize-lines: 2

    server {
        listen {{site_port}};
        root /usr/share/nginx/www;
        index index.html index.htm;
        server_name localhost;
        location / {
            try_files $uri $uri/ /index.html;
        }
    }

The config file is also Jinja2 template and line 2 contains `site_port`
variable.

Edit **/tmp/configme/settings/development.settings**

.. code-block :: ini
   :linenos:

    [etc/nginx.conf]

    gzip_status = off

    [etc/sites-available/my-sites.conf]

    site_port = 8080

The `development.settings` settings file is in the INI format and contains
sections for each of the configuration files that development role will
have generated. If the file is not included in here it will not generated.

Edit **/tmp/configme/settings/production.settings**

.. code-block :: ini
   :linenos:

    [etc/nginx.conf]

    gzip_status = on

    [etc/sites-available/my-sites.conf]

    site_port = 80

The `production.settings` settings file is in the INI format and contains
settings for the production role. As you can see the two configurations
only differ slightly.

Generate Configuration Sets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate the **development** configuration set:

.. code-block :: console

    $ configme \
        --templates-path=/tmp/configme/templates \
        --settings-path=/tmp/configme/settings \
        --output-path=/tmp/configme/output \
        --role-name development

Now check the result in /tmp/configme/output

.. code-block :: console

    /tmp/configme/output/
    `-- development
        `-- etc
            |-- nginx.conf
            `-- sites-available
                `-- my-sites.conf


Now generate the **production** configuration set:

.. code-block :: console

    $ configme \
        --templates-path=/tmp/configme/templates \
        --settings-path=/tmp/configme/settings \
        --output-path=/tmp/configme/output \
        --role-name production


Now check the result in /tmp/configme/output

.. code-block :: console

    /tmp/configme/output/
    `-- production
        `-- etc
            |-- nginx.conf
            `-- sites-available
                `-- my-sites.conf

General Usage
-------------

To see usage run **configme --help**

.. code-block :: console

    usage: configme [-h] -t TEMPLATES_PATH -s SETTINGS_PATH -o OUTPUT_PATH -r
                    ROLE_NAME [-u ROLE_SUFFIX]
                    [-b ROLE_VARIABLES [ROLE_VARIABLES ...]]

    configme 0.4dev command line utility.

    optional arguments:
      -h, --help            show this help message and exit
      -t TEMPLATES_PATH, --templates-path TEMPLATES_PATH
                            Path to configuration templates folder.
      -s SETTINGS_PATH, --settings-path SETTINGS_PATH
                            Path to settings folder.
      -o OUTPUT_PATH, --output-path OUTPUT_PATH
                            Path to output folder.
      -r ROLE_NAME, --role-name ROLE_NAME
                            Role name.
      -u ROLE_SUFFIX, --role-suffix ROLE_SUFFIX
                            Role suffix.
      -b ROLE_VARIABLES [ROLE_VARIABLES ...],
      --role-variables ROLE_VARIABLES [ROLE_VARIABLES ...]
                            Variables that will interpolated into the settings
                            files.

Support and Documentation
-------------------------

Documentation is in progress of being written and is available here: `ConfigMe documentation <http://configme.readthedocs.org/>`_.

To report bugs, and obtain support please use: `GitHub Issues for ConfigMe
<http://github.com/goodwillcoding/configme/issues>`_

Source Code
-----------

Source code is located on GitHub: http://github.com/goodwillcoding/configme


API
---

API will be available at a later date when the implementation stabilizes.

License
-------

ConfigMe is offered under the BSD-derived `Repoze Public License
<http://repoze.org/license.html>`_.

Authors
-------

ConfigMe is produced by the
`Goodwill Coding <http://github.com/goodwillcoding>`_.

ConfigMe is developed by `Michael R`.
