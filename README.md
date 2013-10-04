nbdiff
======

A diffing and merging tool for the IPython Notebook.

# How to run the tests locally

The idea is that while the tests run in a browser-like environment, you can
execute them on the command-line. This also means that travis-ci.org can run
these tests automatically when you submit a pull request.

## How-to

Install node and npm.

In this directory, run:

    $ npm install

to install the dependencies.

To run the tests, run this. You should get the following output.

    $ grunt

    Running "qunit:files" (qunit) task
    Testing src/test/index.html ...OK
    >> 14 assertions passed (21ms)

    Done, without errors.

![Build-status](https://api.travis-ci.org/tarmstrong/nbdiff.png)
