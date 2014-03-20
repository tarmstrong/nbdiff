'''
This is an example of a python test
that compares a diff function (in this case
a hardcoded one that doesn't work) to the
reference JSON to check compliance.
'''
from nose.tools import eq_
import json

from nbdiff.diff import diff


def test_diffs():
    test_cases = json.load(open('test_cases_simple.json'))
    for test_case in test_cases:
        def gentest():
            result = diff(test_case['before'], test_case['after'])
            for (expected, actual) in zip(test_case['diff'], result):
                eq_(expected, actual)
        yield gentest


def test_diffs_cells():
    test_cases = json.load(open('test_cases_cells.json'))
    for i, test_case in enumerate(test_cases):
        result = diff(test_case['before'], test_case['after'])
        def gentest():
            result = diff(test_case['before'], test_case['after'])
            for (expected, actual) in zip(test_case['diff'], result):
                eq_(expected, actual, i)
        yield gentest
