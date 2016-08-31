from unittest import TestCase

from pyrestorm.exceptions.http import AuthorizationException
from .models import Post, Gene, Subject


class RestModelTestCase(TestCase):
    def test_restmodel(self):
        Post()

    def test_restmodel_nested(self):
        instance = Post(
            _json={
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

    def test_restmodel_filter(self):
        genes = Gene.objects.filter(name__icontains='PEX')
        self.assertEqual(len(genes), 15)
        gene = genes.filter(name='PEX10')
        self.assertEqual(len(gene), 1)

    def test_restmodel_getabsoluteurl(self):
        gene = Gene.objects.get(name='PEX10')
        self.assertEqual('https://api.genepeeks.com/genes/PEX10/', gene.get_absolute_url())

    def test_restmodel_get(self):
        gene = Gene.objects.get(name='PEX10')
        self.assertEqual(gene.name, 'PEX10')

    def test_count(self):
        queryset = Gene.objects.all()
        self.assertEqual(queryset.count(), 4813)

    def test_restmodel_get_doesnotexist(self):
        self.assertRaises(Gene.DoesNotExist, Gene.objects.get, name='PEXCFTR\u2019')

    def test_restmodel_get_multipleobjectreturned(self):
        self.assertRaises(Gene.MultipleObjectsReturned, Gene.objects.get, name__icontains='PEX')

    def test_restmodel_save(self):
        post = Post.objects.get(id=1)
        post.title = 'Testing'
        post.save()
        self.assertEqual(post._data['title'], post.title)

    def test_restmodel_serializable_value(self):
        post = Post.objects.get(id=1)
        post.title = 'Testing'
        post.save()
        self.assertEqual(post.serializable_value('title'), post.title)

    def test_restmodel_createnewinstance(self):
        post = Post.objects.create(title='Hello', body='World', userId=1)
        self.assertEqual(post.id, 101)

    def test_restmodel_savenewinstance(self):
        post = Post(title='Hello', body='World', userId=1)
        post.save()
        self.assertEqual(post.id, 101)

    def test_restmodel_get_or_create_false(self):
        gene, created = Gene.objects.get_or_create(name='PEX10')
        self.assertEqual(gene.name, 'PEX10')
        self.assertFalse(created)

    def test_restmodel_get_or_create_true(self):
        post, created = Post.objects.get_or_create(userId=100, defaults={'title': 'Hello', 'body': 'World'})
        self.assertEqual(post.id, 101)
        self.assertEqual(post.title, 'Hello')
        self.assertEqual(post.body, 'World')
        self.assertTrue(created)

    def test_restormmanager_get_on_instance(self):
        instance = Post()
        self.assertRaises(AttributeError, getattr, instance, 'objects')

    def test_authorization_headers(self):
        self.assertRaises(AuthorizationException, Subject.objects.get, key='TESTING')
