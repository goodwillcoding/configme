GonfigMe
========

About
-----

ConfigMe is a small, fast, down-to-earth, open source Python config generation
framework and command line utility. It makes generation of real-world
configuration files and deployment more fun, more predictable, and more
productive.

Project Status
--------------

Project is still in development at 85% completion. That means it works but
there no guarantees it won't break.


Installation
-------------

1. Clone the repo
2. Setup a virtualenv environment
3. python ./setup develop

Examples
--------

Generate config for "dev" and "stage" role and run diff command to see the
difference.

::

    configme -t ./examples/templates/ -s ./examples/settings/ -o ./examples/output/ --role-name dev

    configme -t ./examples/templates/ -s ./examples/settings/ -o ./examples/output/ --role-name stage

    diff -u ./examples/output/dev/test.conf ./examples/output/stage/test.conf

Support and Documentation
-------------------------

Documentation is in progress of being written and is available here: `ConfigMe documentation <http://configme.readthedocs.org/>`_.

To report bugs, and obtain support please see `issue tracker <http://github.com/goodwillcoding/configme>`_

Test coverage
-------------

Current unittest coverage stands at 91% using nose + nosexcover line coverage
tool.

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
