from pyrestorm.fields import IntegerField, OneToManyField
from pyrestorm.models import RestModel
from pyrestorm.paginators import DjangoRestFrameworkLimitOffsetPaginator


class Comment(object):
    def __init__(self, body):
        self.body = body


class Author(object):
    def __init__(self, name):
        self.name = name


class Post(RestModel):
    class Meta:
        url = 'http://jsonplaceholder.typicode.com/posts'

    id = IntegerField()


class Variant(RestModel):
    class Meta:
        paginator_class = DjangoRestFrameworkLimitOffsetPaginator
        url = 'https://api.genepeeks.com/variants/'


class Gene(RestModel):
    class Meta:
        paginator_class = DjangoRestFrameworkLimitOffsetPaginator
        slug_field = 'ens_gene'
        url = 'https://api.genepeeks.com/genes/'

    variants = OneToManyField(Variant)


class Subject(RestModel):
    class Meta:
        paginator_class = DjangoRestFrameworkLimitOffsetPaginator
        slug_field = 'key'
        token = 'INVALIDTOKEN'
        url = 'https://api.genepeeks.com/subjects/'
