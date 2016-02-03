testrail-reporting
==================

Web App that lets you build custom reports for TestRail.

Requirements
------------

You will need the following things properly installed on your machine:

* Python 3.5+
* MongoDB 3+
* Node.js 5+ (with NPM)

Installation
------------

Development Environment
~~~~~~~~~~~~~~~~~~~~~~~

1. Install system requirements:

.. code-block:: shell

    $ sudo apt-get install build-essential python3.5-dev python3-pip mongodb nodejs
    $ sudo pip3 install virtualenv

2. Install Python requirements:

.. code-block:: shell

    $ cd testrail-reporting
    $ virtualenv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt

3. Install JavaScript requirements and build static:

.. code-block:: shell

    $ npm install
    $ npm run watch

4. Make sure that MongoDB is running:

.. code-block:: shell

    $ sudo service mongodb start

5. Create local configuration file in `/etc/testrail_reporting/testrail_reporting.conf`
   or `~/testrail_reporting.conf` and populate it with Google and TestRail
   credentials. If you want to create your own credentials for Google oauth,
   go to https://console.developers.google.com "APIs & Auth" -> Credentials
   and create new credentials there.

6. Sync the database with TestRail:

.. code-block:: shell

   $ python manage.py sync

7. Start your local development server:

.. code-block:: shell

   $ python manage.py runserver

Production Environment
~~~~~~~~~~~~~~~~~~~~~~

TODO

Hacking
-------

To run tests and linters:

.. code-block:: shell

    $ pip install tox
    $ tox
    $ npm run lint
