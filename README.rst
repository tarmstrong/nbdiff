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

NBDiff ships with an IPython Notebook extension used modify the Notebook interface for merging.
To create a profile with this extension installed, run the following:

::

    nbdiff-install

Configure Git/Mercurial
~~~~~~~~~~~~~~~~~~~~~~~

NBMerge is compatible with Mercurial out of the box by running ``hg merge --tool=nbmerge <branch>``.

Git, however, needs to be configured by adding the following to your ``.gitconfig`` file:

::

    [mergetool "nbmerge"]                                                           
      cmd = nbmerge $LOCAL $BASE $REMOTE $MERGED

Alternatively, you can run the following command to add this configuration automatically:

::

    git config --global mergetool.nbmerge.cmd = "nbmerge \$LOCAL \$BASE \$REMOTE \$MERGED"

You can then run ``nbmerge`` from git like so:

::

    git mergetool --tool=nbmerge


Usage
-----

NBDiff
~~~~~~

::

    usage: nbdiff [-h] [--cached] before after

      Produce a diffed notebook from before and after notebooks.

      If no arguments are given, nbdiff asks git for a list
      of modified files.

    positional arguments:
      before  first version of the notebook
      after   second version of the notebook

    optional arguments:
      -h, --help  show this help message and exit
      --cached    instead of unstaged changes, look at staged changes.

NBMerge
~~~~~~~

::

    usage: nbmerge [-h] [local base remote [result]]

      If no arguments are given, nbmerge asks git for a list of unmerged files
      and uses those as input.

    positional arguments:
      local   the local branch's version of the notebook
      base    the common ancestor version of local and remote notebooks
      remote  the remote branch's version of the notebook

    optional arguments:
      -h, --help  show this help message and exit


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

