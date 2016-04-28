from unittest import TestCase

from pyrestorm.models import RestModel
from pyrestorm.query import RestQueryset


class TestModel(RestModel):
    url = 'http://jsonplaceholder.typicode.com/posts'


class RestQuerysetTestCase(TestCase):
    def test_init(self):
        RestQueryset(TestModel)

    def test_getitem(self):
        queryset = RestQueryset(TestModel)
        self.assertEqual(queryset[0].id, 1)

    def test_len(self):
        queryset = RestQueryset(TestModel)
        self.assertEqual(len(queryset), 100)

    def test_repr(self):
        queryset = RestQueryset(TestModel)
        repr(queryset)
        self.assertTrue(True)

    def test_unicode(self):
        queryset = RestQueryset(TestModel)
        unicode(queryset)

    def test_iter(self):
        queryset = RestQueryset(TestModel)
        for item in queryset:
            self.assertTrue(True)
