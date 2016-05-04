from unittest import TestCase

from .models import Post, Gene


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

    def test_restmodel_get(self):
        gene = Gene.objects.get(name='PEX10')
        self.assertEqual(gene.name, 'PEX10')

    def test_restmodel_get_doesnotexist(self):
        self.assertRaises(Gene.DoesNotExist, Gene.objects.get, name='PEXCFTR')

    def test_restmodel_get_multipleobjectreturned(self):
        self.assertRaises(Gene.MultipleObjectsReturned, Gene.objects.get, name__icontains='PEX')

    def test_restormmanager_get_on_instance(self):
        instance = Post()
        self.assertRaises(AttributeError, getattr, instance, 'objects')
