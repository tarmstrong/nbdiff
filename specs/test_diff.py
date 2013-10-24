'''
This is an example of a python test
that compares a diff function (in this case
a hardcoded one that doesn't work) to the
reference JSON to check compliance.
'''
from nose.tools import eq_
import json

def diff(before, after):
    return []

def test_diffs():
    test_cases = json.load(open('test_cases.json'))
    for test_case in test_cases:
        result = diff(test_case['before'], test_case['after'])
        eq_(result, test_case['diff'])
