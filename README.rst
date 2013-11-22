===============================
NBDiff
===============================

.. image:: https://badge.fury.io/py/nbdiff.png
    :target: http://badge.fury.io/py/nbdiff
    
.. image:: https://travis-ci.org/tarmstrong/nbdiff.png?branch=master
        :target: https://travis-ci.org/tarmstrong/nbdiff

.. image:: https://pypip.in/d/nbdiff/badge.png
        :target: https://crate.io/packages/nbdiff?version=latest


A tool for diffing and merging IPython Notebook files.

This project is currently under heavy development by a team of
university students. See
`AUTHORS <https://github.com/tarmstrong/nbdiff/blob/master/AUTHORS.rst>`__
for more information.

* Free software: MIT license
* Documentation: http://nbdiff.rtfd.org.

Installation
------------

Using Pip
~~~~~~~~~

If you have pip installed:

::

    pip install nbdiff

From Source
~~~~~~~~~~~

1. Download the code from this repository
2. Run ``python setup.py install``

Install the Extension
~~~~~~~~~~~~~~~~~~~~~

NBDiff's merging interface currently works as an IPython Notebook extension.

TODO write instructions on how to install the extension.

Features
--------

TODO

Developing
----------

Run the Python tests
~~~~~~~~~~~~~~~~~~~~

To run the python tests, run the following command:

::

    $ python setup.py nosetests

NBDiff adheres to `PEP-8 <http://www.python.org/dev/peps/pep-0008/>`__. To check the code
against PEP-8, use ``flake8`` like so:

::

    $ flake8 tests nbdiff

Run the JavaScript tests
~~~~~~~~~~~~~~~~~~~~~~~~

First, install `node <http://nodejs.org/>`__ and npm.

Second, install the JavaScript dependencies using ``npm``.

::

    $ npm install

Finally, run the tests with ``grunt``. You should output similar to the following.
Note that ``grunt`` will not only run the tests, but check for common style problems with ``jshint``.

::

    $ grunt

    Running "qunit:files" (qunit) task
    Testing src/test/index.html ...OK
    >> 14 assertions passed (21ms)

    Done, without errors.

