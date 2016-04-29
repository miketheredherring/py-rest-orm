from pyrestorm.models import RestModel
from pyrestorm.paginators import DjangoRestFrameworkLimitOffsetPaginator


class Post(RestModel):
    url = 'http://jsonplaceholder.typicode.com/posts'


class Gene(RestModel):
    url = 'https://api.genepeeks.com/genes/'
    paginator_class = DjangoRestFrameworkLimitOffsetPaginator
