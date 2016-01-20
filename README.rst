testrail-reporting
==================

Web App that lets you build custom reports for TestRail.

Requirements
------------

You will need the following things properly installed on your machine:

* Python 2.7
* MongoDB
* Node.js (with NPM)

Installation
------------

Development Environment
~~~~~~~~~~~~~~~~~~~~~~~

1. Install system requirements:

.. code-block:: shell

    $ sudo apt-get install build-essential python-dev python-pip mongodb
    $ sudo pip install virtualenv

2. Install Python requirements:

.. code-block:: shell

    $ cd testrail-reporting
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

3. Install JavaScript requirements and build static:

.. code-block:: shell

    $ npm install
    $ npm run build

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

Hacking
-------

To run tests and linters:

.. code-block:: shell

    $ pip install tox
    $ tox
