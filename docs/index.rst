.. index::
   single: About
   single: Project Status
   single: Support and Documentation
   single: Bugs
   single: Source Code
   single: API
   single: License
   single: Authors

.. _front:

===========================================================
The ConfigMe Configuration Generation Framework and Utility
===========================================================


ConfigMe is a small, fast, down-to-earth, open source configuration generation
framework and command line utility. It makes generation of real-world
configuration files and deployment more fun, more predictable, and more
productive.


What Problem Does ConfigMe Solve For You?
=========================================

Whether used in production, staging or development the majority of the
configuration files are usually **95% to 99%** identical and it can prove
**time consuming and error-prone** to maintain them in sync.

ConfigMe solves this problem for you.


Whats Next?
===========

Learn ConfigMe by following the :ref:`tutorial`


Narrative Documentation
=======================

.. toctree::
   :maxdepth: 2

   tutorial
   usage


Support and Documentation
=========================

| Read the official ConfigMe documentation here: http://configme.readthedocs.org

| Ask for help on IRC: irc.freenode.org in #pyramid channel, mention
  "**configme**" in your question, to alert people who can help.
| You can use the IRC WebChat here:
  `http://webchat.freenode.net/?channels=pyramid
  <http://webchat.freenode.net/?channels=pyramid&uio=d4>`_

| To report bugs, and obtain support please use ConfigMe issue tracker here:
  http://github.com/goodwillcoding/configme/issues


How it Works
============

ConfigMe is written in Python, uses Jinja2 for templates and INI files
for settings configuration. Support for Django, Mako and other templates is
planned.


Current Project Status
======================

Project is still in development at 90% completion. That means it works but
there no guarantees it won't break. The names, command-line options and code
interfaces may change so backward compatibility is currently not guaranteed.


Test Coverage
-------------

.. include :: tests_status.rst

Source Code
===========

Source code is located on GitHub: http://github.com/goodwillcoding/configme


API
===

API will be available at a later date when the implementation stabilizes.


License
=======

ConfigMe is offered under the BSD-derived `Repoze Public License
<http://repoze.org/license.html>`_.


Authors
=======

ConfigMe is produced by the
`Goodwill Coding <http://github.com/goodwillcoding>`_.

ConfigMe is developed by `Michael R`.

Indices and tables
==================

* :ref:`glossary`
* :ref:`genindex`
* :ref:`search`


.. toctree::
   :hidden:

   tests_status
