.. _tutorial:

========
Tutorial
========

This document provides a brief tutorial on how to use ConfigMe.

Installation
============

1. Clone the ConfigMe repo
2. Setup a virtualenv environment
3. python ./setup develop

Defining The Problem
====================

To demonstrate the use of of `ConfigMe` we will generate set of development and
production configuration for NginX for a project called `my-site`.

Now lets look at a typical NginX configuration setup.

.. code-block :: console

    /etc/
    `-- nginx
        |-- nginx.conf
        `-- sites-available
            `-- my-site.conf

However for nginx.conf production configuration we want gzipping on while
development configuration will have it off.

Additionally we want my-site to be served on port 80 in production and port
8080 in development.


Configuration Folder Skeleton
=============================

First create the folder skeleton that will contain the templates, settings
and output:

.. code-block :: console

    $ cd /tmp

    $ mkdir -p /tmp/configme/templates/etc/nginx/sites-available
    $ mkdir -p /tmp/configme/settings
    $ mkdir -p /tmp/configme/output


Create **etc/nginx/nginx.conf** template
========================================

.. code-block :: console

    $ $EDITOR /tmp/configme/templates/etc/nginx/nginx.conf

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


.. note ::

    The config file is a Jinja2 template and as you can see line 22 contains
    **gzip_status** variable.


Create **etc/nginx/sites-available/my-site.conf** template
==========================================================

.. code-block :: console

    $ $EDITOR /tmp/configme/templates/etc/nginx/sites-available/my-site.conf

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

.. note ::

    The config file is also Jinja2 template and line 2 contains **site_port**
    variable.


Add **development** Role Settings
=================================

Now lets create the development.settings file and set the **gzip_status** and
**site_port** variables to their respective development values.

.. code-block :: console

    $ $EDITOR /tmp/configme/settings/development.settings

.. code-block :: ini
   :linenos:

    [etc/nginx.conf]

    gzip_status = off

    [etc/sites-available/my-site.conf]

    site_port = 8080


.. note ::

    The `development.settings` settings file uses the INI format and contains
    sections for each of the configuration files that development role will
    have generated. **If the file is not included in here it will not
    generated.**


Add **production** Role Settings
================================

Now lets create the production.settings file and set the **gzip_status** and
**site_port** variables to their respective production values.


.. code-block :: console

    $ $EDITOR /tmp/configme/settings/production.settings

.. code-block :: ini
   :linenos:

    [etc/nginx/nginx.conf]

    gzip_status = on

    [etc/nginx/sites-available/my-site.conf]

    site_port = 80

.. note ::

    The `production.settings` settings file uses the INI format and contains
    settings for the production role. As you can see the two configurations
    only differ slightly.


Resulting Configuration Skeleton
================================

Now check the result in /tmp/configme/

.. code-block :: console

    /tmp/configme/
    |-- output
    |-- settings
    |   |-- development.settings
    |   `-- production.settings
    `-- templates
        `-- etc
            `-- nginx
                |-- nginx.conf
                `-- sites-available
                    `-- my-site.conf


Generate **development** Configuration
======================================

.. code-block :: console

    $ configme \
        --templates-path=/tmp/configme/templates \
        --settings-path=/tmp/configme/settings \
        --output-path=/tmp/configme/output \
        --role-name development


Generate **production** Configuration
=====================================

.. code-block :: console

    $ configme \
        --templates-path=/tmp/configme/templates \
        --settings-path=/tmp/configme/settings \
        --output-path=/tmp/configme/output \
        --role-name production


Resulting Configuration Sets
============================

.. code-block :: console

    /tmp/configme/output/
    |-- development
    |   `-- etc
    |       `-- nginx
    |           |-- nginx.conf
    |           `-- sites-available
    |               `-- my-site.conf
    `-- production
        `-- etc
            `-- nginx
                |-- nginx.conf
                `-- sites-available
                    `-- my-site.conf


More on Usage
=============

For usage see: :ref:`usage`
