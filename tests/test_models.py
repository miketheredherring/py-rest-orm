from unittest import TestCase

from pyrestorm.models import RestModel


class TestModel(RestModel):
    url = 'http://jsonplaceholder.typicode.com/posts'


def create_bad_restmodel():
    class BadTestModel(RestModel):
        pass


class RestModelTestCase(TestCase):
    def test_restmodel_invalid_url(self):
        self.assertRaises(NotImplementedError, create_bad_restmodel)

    def test_restmodel(self):
        TestModel()

    def test_restmodel_nested(self):
        instance = TestModel(
            data={
                'var1': 'helloworld',
                'nested_object': {
                    'var2': 'hellouniverse'
                }
            }
        )
        self.assertTrue(hasattr(instance, 'var1'))
        self.assertTrue(hasattr(instance.nested_object, 'var2'))

    def test_restmodel_all(self):
        instances = TestModel.objects.all()
        self.assertEqual(len(instances), 100)

    def test_restormmanager_get_on_instance(self):
        instance = TestModel()
        self.assertRaises(AttributeError, getattr, instance, 'objects')
