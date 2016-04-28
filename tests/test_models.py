from unittest import TestCase

from pyrestorm.models import RestModel


class TestModel(RestModel):
    url = 'http://jsonplaceholder.typicode.com/posts'


class RestModelTestCase(TestCase):
    def test_restmodel_invalid_url(self):
        self.assertRaises(NotImplementedError, RestModel)

    def test_restmodel(self):
        instance = TestModel()

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
