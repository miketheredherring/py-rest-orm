from unittest import TestCase

from .models import Post


class RestModelTestCase(TestCase):
    def test_restmodel(self):
        Post()

    def test_restmodel_nested(self):
        instance = Post(
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
        instances = Post.objects.all()
        self.assertEqual(len(instances), 100)

    def test_restormmanager_get_on_instance(self):
        instance = Post()
        self.assertRaises(AttributeError, getattr, instance, 'objects')
