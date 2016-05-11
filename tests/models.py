from pyrestorm.models import RestModel
from pyrestorm.paginators import DjangoRestFrameworkLimitOffsetPaginator


class Post(RestModel):
    class Meta:
        url = 'http://jsonplaceholder.typicode.com/posts'


class Gene(RestModel):
    class Meta:
        paginator_class = DjangoRestFrameworkLimitOffsetPaginator
        slug_field = 'slug'
        url = 'https://api.genepeeks.com/genes/'
