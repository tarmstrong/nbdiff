import hglib
import os
import unittest

from nbdiff.adapter.hg_adapter import HgAdapter
from testfixtures import tempdir


class TestHgAdapterFunctions(unittest.TestCase):

    def setUp(self):
        self.original_path = os.getcwd()

    def tearDown(self):
        os.chdir(self.original_path)

    @tempdir()
    def test_get_modified_notebooks_empty(self, d):
        os.chdir(os.path.join(d.path))
        hglib.init()
        adapter = HgAdapter()
        result = adapter.get_modified_notebooks()
        self.assertTrue(result == [])

    @tempdir()
    def test_get_modified_notebooks_deleted(self, d):
        os.chdir(d.path)
        client = hglib.init()
        client.open()
        d.makedir('first')
        d.makedir('first/second')
        path = d.write('first/second/1.ipynb', 'initial')
        self.assertEqual(d.read('first/second/1.ipynb'), 'initial')
        client.add('first/second/1.ipynb')
        client.commit("message")
        file = open(path, 'w')
        file.write("modified")
        file.close()
        self.assertEqual(d.read('first/second/1.ipynb'), 'modified')
        os.chdir(os.path.join(d.path, 'first'))
        os.remove(path)

        adapter = HgAdapter()
        result = adapter.get_modified_notebooks()
        self.assertTrue(len(result) == 0)

    @tempdir()
    def test_get_modified_notebooks(self, d):
        os.chdir(d.path)
        client = hglib.init()
        client.open()
        d.makedir('first')
        d.makedir('first/second')
        path = d.write('first/second/1.ipynb', 'initial')
        self.assertEqual(d.read('first/second/1.ipynb'), 'initial')
        client.add('first/second/1.ipynb')
        client.commit("message")
        file = open(path, 'w')
        file.write("modified")
        file.close()
        self.assertEqual(d.read('first/second/1.ipynb'), 'modified')
        os.chdir(os.path.join(d.path, 'first'))

        adapter = HgAdapter()
        result = adapter.get_modified_notebooks()
        self.assertTrue(len(result) == 1)
        self.assertEqual(result[0][0].read(), 'modified')
        self.assertEqual(result[0][1].read(), 'initial')
        self.assertEqual(result[0][2], 'first/second/1.ipynb')

    @tempdir()
    def test_get_unmerged_notebooks_empty(self, d):
        os.chdir(os.path.join(d.path))
        hglib.init()
        adapter = HgAdapter()
        result = adapter.get_unmerged_notebooks()
        self.assertTrue(result == [])
