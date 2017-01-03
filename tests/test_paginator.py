from unittest import TestCase

from pyrestorm.paginators import DjangoRestFrameworkLimitOffsetPaginator, RestPaginator


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

    def test_restpaginator_setmax(self):
        paginator = RestPaginator()
        paginator.set_max(100)
        self.assertEqual(paginator.max, 100)

    def test_restpaginator_asparams(self):
        paginator = RestPaginator()
        self.assertFalse(paginator.as_params())


class DjangoRestFrameworkPaginatorTestCase(TestCase):
    def test_djangorestpaginator_init(self):
        DjangoRestFrameworkLimitOffsetPaginator()

    def test_djangorestpaginator_next(self):
        paginator = DjangoRestFrameworkLimitOffsetPaginator(limit=30)
        self.assertFalse(paginator.next())
        paginator.set_max({'count': 50})
        self.assertTrue(paginator.next())
        self.assertEqual(paginator.position, 30)
        self.assertFalse(paginator.next())

    def test_djangorestpaginator_prev(self):
        paginator = DjangoRestFrameworkLimitOffsetPaginator()
        paginator.cursor(30)
        self.assertTrue(paginator.prev())
        paginator.cursor(1)
        self.assertTrue(paginator.prev())
        self.assertFalse(paginator.prev())

    def test_djangorestpaginator_setmax(self):
        paginator = DjangoRestFrameworkLimitOffsetPaginator()
        paginator.set_max({'count': 100, 'results': []})
        self.assertEqual(paginator.max, 100)
