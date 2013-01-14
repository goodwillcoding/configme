The GonfigMe Configuration Generation Framework and Utility
===========================================================

ConfigMe is a small, fast, down-to-earth, open source configuration generation
framework and command line utility. It makes generation of real-world
configuration files and deployment more fun, more predictable, and more
productive.


What problem does ConfigMe solve for you?
-----------------------------------------

Whether used in production, staging or development the majority of the
configuration files are usually **95%** identical and it can prove time
consuming and error-prone to maintain them in sync.

ConfigMe solves this for you by applying role's settings against the templates
containing the configuration and generates the configuration set you need.


Tutorial
--------

Follow this `tutorial <http://configme.readthedocs.org/tutorial.html>`_ to
learn how to use ConfigMe.

About
-----

ConfigMe is written in Python, uses Jinja2 for templates and INI files
for settings configuration. Support for Django, Mako and other templates is
planned.


Project Status
--------------

Project is still in development at 85% completion. That means it works but
there no guarantees it won't break. The names, command-line options and code
interfaces may change so backward compatibility is currently not guaranteed.


Test Coverage
~~~~~~~~~~~~~

**Current unit-test coverage stands at 91% using nose + nosexcover line
coverage tool.**


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
