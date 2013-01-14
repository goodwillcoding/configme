The GonfigMe Configuration Generation Framework and Utility
===========================================================

About
-----

ConfigMe is a small, fast, down-to-earth, open source config generation
framework and command line utility. It makes generation of real-world
configuration files and deployment more fun, more predictable, and more
productive. ConfigMe is written in Python.

Project Status
--------------

Project is still in development at 85% completion. That means it works but
there no guarantees it won't break. Also names and options and conventions may
change so backward compatibility is currently not guaranteed.

Test Coverage
~~~~~~~~~~~~~

**Current unittest coverage stands at 91% using nose + nosexcover line coverage
tool.**

Source Code
-----------

Source code is located on GitHub: http://github.com/goodwillcoding/configme

Installation
------------

1. Clone the repo
2. Setup a virtualenv environment
3. python ./setup develop
4. Run `configme --help`

Usage
-----

You can see examples in the ./examples folder of the project

Sample Configuration Template (Jinja2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Sample config**: ./examples/templates/test.conf

.. code-block :: jinja

    # this is a test config file

    ConfigApp "HelloWorld"
    AppVerion {{app_version}}

Sample "dev" Config Template Settings (INI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuration settings file for "dev" role.

A section name for each config file that needs to be generated must be
specified and any settings that need to be interpolated into the template. In
our case **app_version**.

**Sample config settings**: ./examples/settings/dev.settings

.. code-block :: ini

    [test.conf]

    app_version=dev


Sample "stage" Config Template Settings (INI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same as above but for "stage" role.

**Sample config settings**: ./examples/settings/stage.settings

.. code-block :: ini

    [test.conf]

    app_version=stage

Generating Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Generate config for "dev" and "stage" role by running `configme` utility and
and telling it where to find the configuration templates, the settings file
as well where to output the configs.

.. code-block :: console

    $ configme \
        --templates-path=./examples/templates \
        --settings-path=./examples/settings \
        --output-path=./examples/output \
        --role-name dev

    $ configme \
        --templates-path=./examples/templates \
        --settings-path=./examples/settings \
        --output-path=./examples/output \
        --role-name stage

The generator has dones the following

1. Create a "role" folder in the output folder of `./examples/output`
   The role folder name is the same as role name
2. Interpolate the settings file variables into the template
3. Write out the config files


Now run the diff command to see the difference.

.. code-block :: console

    $ diff -u
        ./examples/output/dev/test.conf \
        ./examples/output/stage/test.conf

.. code-block :: diff

    --- ./examples/output/dev/test.conf 2013-01-12 15:54:01.976148562 -0800
    +++ ./examples/output/stage/test.conf   2013-01-12 16:13:51.639879447 -0800
    @@ -1,4 +1,4 @@
     # this is a test config file

     ConfigApp "HelloWorld"
    -AppVerion dev
    \ No newline at end of file
    +AppVerion stage
    \ No newline at end of file

As you can see the only difference is are the variables specified in the
specific settings file.

For more options run **configme --help**

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

To report bugs, and obtain support please see `issue tracker on GitHub Issues
<http://github.com/goodwillcoding/configme/issues>`_

API
---

API will be available at the later date when the implementation stabilizes.

License
-------

ConfigMe is offered under the BSD-derived `Repoze Public License
<http://repoze.org/license.html>`_.

Authors
-------

ConfigMe is produced by the
`Goodwill Coding <http://github.com/goodwillcoding>`_.

ConfigMe is developed by `Michael R`.
