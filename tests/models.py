from pyrestorm.models import RestModel
from pyrestorm.paginators import DjangoRestFrameworkLimitOffsetPaginator


class Post(RestModel):
    class Meta:
        url = 'http://jsonplaceholder.typicode.com/posts'


class Gene(RestModel):
    class Meta:
        url = 'https://api.genepeeks.com/genes/'
        paginator_class = DjangoRestFrameworkLimitOffsetPaginator
