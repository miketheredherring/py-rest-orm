from unittest import TestCase

from pyrestorm.paginator import DjangoRestFrameworkLimitOffsetPaginator, RestPaginator


class RestPaginatorTestCase(TestCase):
    def test_restpaginator_init(self):
        RestPaginator()

    def test_restpaginator_next(self):
        paginator = RestPaginator()
        self.assertRaises(NotImplementedError, paginator.next)

    def test_restpaginator_prev(self):
        paginator = RestPaginator()
        self.assertRaises(NotImplementedError, paginator.prev)

    def test_restpaginator_cursor(self):
        paginator = RestPaginator()
        paginator.cursor(10)
        self.assertEqual(paginator.position, 10)


class DjangoRestFrameworkPaginatorTestCase(TestCase):
    def test_djangorestpaginator_init(self):
        DjangoRestFrameworkLimitOffsetPaginator()

    def test_djangorestpaginator_next(self):
        paginator = DjangoRestFrameworkLimitOffsetPaginator(limit=30)
        self.assertTrue(paginator.next())
        self.assertEqual(paginator.position, 30)
        paginator.count = 50
        self.assertFalse(paginator.next())

    def test_djangorestpaginator_prev(self):
        paginator = DjangoRestFrameworkLimitOffsetPaginator()
        paginator.cursor(30)
        self.assertTrue(paginator.prev())
        paginator.cursor(1)
        self.assertTrue(paginator.prev())
        self.assertFalse(paginator.prev())

    def test_djangorestpaginator_as_url(self):
        paginator = DjangoRestFrameworkLimitOffsetPaginator()
        self.assertEqual(paginator.as_url(), 'limit=20&offset=0')
