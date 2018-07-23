from unittest import TestCase

from pyrestorm.exceptions.http import AuthorizationException
from .models import Post, Gene, Subject, Comment, Author


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
        genes = Gene.objects.filter(ens_gene='ENSG00000011295')
        self.assertEqual(len(genes), 1)

    def test_restmodel_filter_empty(self):
        genes = Gene.objects.filter(ens_gene='ENSG00000011295', id__in=frozenset([1, 2]))
        self.assertEqual(len(genes), 1)

    def test_restmodel_getabsoluteurl(self):
        gene = Gene.objects.get(ens_gene='ENSG00000011295')
        self.assertEqual('https://api.genepeeks.com/genes/ENSG00000011295/', gene.get_absolute_url())

    def test_restmodel_get(self):
        gene = Gene.objects.get(ens_gene='ENSG00000011295')
        self.assertEqual(gene.ens_gene, 'ENSG00000011295')

    def test_restmodel_relatedfield_count(self):
        gene = Gene.objects.get(ens_gene='ENSG00000011295')
        self.assertEqual(gene.variants.count(), 781)

    def test_restmodel_relatedfield_filter(self):
        gene = Gene.objects.get(ens_gene='ENSG00000011295')
        variant = gene.variants.all()[0]
        self.assertTrue(bool(variant.slug))

    def test_count(self):
        queryset = Gene.objects.all()
        self.assertEqual(queryset.count(), 6671)

    def test_restmodel_get_doesnotexist(self):
        self.assertRaises(Gene.DoesNotExist, Gene.objects.get, ens_gene='ENSG00000011295\u2019')

    def test_restmodel_get_multipleobjectreturned(self):
        self.assertRaises(Gene.MultipleObjectsReturned, Gene.objects.get, name__icontains='PEX')

    def test_restmodel_save(self):
        post = Post.objects.get(id=1)
        post.id = 2
        post.body = [Comment(body='Are we having fun yet?'), Comment(body='Hoe about now?')]
        post.title = 'Testing'
        post.save()
        # Redundant save for list serializing
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

    def test_restmodel_nestedstructures(self):
        post = Post(title='Hello', body='World', userId=1)
        post.author = Author(name='Michael Hearing')
        post.comments = [Comment(body='Are we having fun yet?'), Comment(body='Hoe about now?')]
        post.fun_numbers = [1, 2, 3, 5, 7]
        post.archived = None
        post.save()
        self.assertEqual(post.id, 101)

    def test_restmodel_get_or_create_false(self):
        gene, created = Gene.objects.get_or_create(ens_gene='ENSG00000011295')
        self.assertEqual(gene.ens_gene, 'ENSG00000011295')
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
