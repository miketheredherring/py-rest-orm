from unittest import TestCase

from pyrestorm.query import RestQueryset

from .models import Post


class RestQuerysetTestCase(TestCase):
    def test_init(self):
        RestQueryset(Post)

    def test_getitem(self):
        queryset = RestQueryset(Post)
        self.assertEqual(queryset[0].id, 1)

    def test_len(self):
        queryset = RestQueryset(Post)
        self.assertEqual(len(queryset), 100)

    def test_repr(self):
        queryset = RestQueryset(Post)
        repr(queryset)
        self.assertTrue(True)

    def test_unicode(self):
        queryset = RestQueryset(Post)
        unicode(queryset)

    def test_iter(self):
        queryset = RestQueryset(Post)
        for item in queryset:
            self.assertTrue(True)


class RestPaginatedQuerysetTestCase(TestCase):
    def test_init(self):
        # RestQueryset(PaginatedQueryTestModel)[0:5]
        pass
