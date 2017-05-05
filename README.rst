django-rest-friendship
======================================

|build-status-image| |pypi-version|

Overview
--------

DRF endpoints for django-friendship

Requirements
------------

-  Python (2.7, 3.5, 3.6)
-  Django (1.9, 1.10, 1.11)
-  Django REST Framework (3.6)

Installation
------------

Install using ``pip``\ …

.. code:: bash

    $ pip install django-rest-friendship
    
Add rest_friendship to your `INSTALLED_APPS`

.. code:: python

    INSTALLED_APPS = (
    ...
    'friendship',  # Django friendship
    'rest_framework',  # Django REST Framework
    'rest_friendship',  # Django REST Friendship
    'rest_framework.authtoken',
    ...
    )

Example
-------

TODO: Write example.

Testing
-------

Install testing requirements.

.. code:: bash

    $ pip install -r requirements.txt

Run with runtests.

.. code:: bash

    $ ./runtests.py

You can also use the excellent `tox`_ testing tool to run the tests
against all supported versions of Python and Django. Install tox
globally, and then simply run:

.. code:: bash

    $ tox

Documentation
-------------

To build the documentation, you’ll need to install ``mkdocs``.

.. code:: bash

    $ pip install mkdocs

To preview the documentation:

.. code:: bash

    $ mkdocs serve
    Running at: http://127.0.0.1:8000/

To build the documentation:

.. code:: bash

    $ mkdocs build

.. _tox: http://tox.readthedocs.org/en/latest/

.. |build-status-image| image:: https://secure.travis-ci.org/dnmellen/django-rest-friendship.svg?branch=master
   :target: http://travis-ci.org/dnmellen/django-rest-friendship?branch=master
.. |pypi-version| image:: https://img.shields.io/pypi/v/django-rest-friendship.svg
   :target: https://pypi.python.org/pypi/django-rest-friendship
