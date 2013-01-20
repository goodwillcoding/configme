.. index::
    single: Usage

.. _usage:

=====
Usage
=====

This document describes basic usage for ConfigMe.

ConfigMe is run using `configme` command-line utility, uses Jinja2 templates
and INI files (using Python's ConfigParser)


Terms
=====

**Role** is a collection of configuration files generated for a specific purpose.
An example of role names can be: `development`, `stage`, `production` or
anything you want.

**Configuration Template** is file containing template for configuration file.
The template may contain variables that will be replaced by values contained in
the role's settings file. Currently only templates are written in Jinja2
templating language. Support for other templating languages is planned.

**Role Settings** is a file in a INI format containing variables for each of
the configuration files



Usage and Command-line Options
==============================

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


File Naming Conventions
=======================

ConfigMe uses INI files and Python's ConfigParsers which places some
limitations on naming of sections in the INI files. Since these sections
names correspond to files located on the filesystems this limitations extends
there as well.

Role Names
----------

The name should be have consist of characters considered valid for
a file name on the operating system it is run on. It must also be a
correct section name in the INI style settings file. Additionally it
must be at least marginally human readable.

As such due to difficulty maintaining OS specific forbidden characters
set, complying with INI file specifications, and keeping readability
a set of forbidden characters have chosen.

The naming rules are:

 - name cannot start with a: `space`
 - name cannot contain: `<` `>` `:` `'` `"` `/` `\\` `|` `?` `*` `\``


File Names and Paths
--------------------

The path should be have consist of characters considered valid for
a file name on the operating system it is run on. It must also be a
correct section name in the INI style settings file. Additionally it
must be at least marginally human readable.

As such due to difficulty maintaining OS specific forbidden characters
set, complying with INI file specifications, and keeping readability
a set of forbidden characters have chosen.

The naming rules are:

 - name cannot start with a: `space` `/` `../` `./`
 - name cannot contain:
   `/../` `/./` `<` `>` `:` `'` `"` `|` `?` `*` `\``
