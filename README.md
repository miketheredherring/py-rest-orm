# py-rest-orm
[![Coverage Status](https://coveralls.io/repos/github/GenePeeks/py-rest-orm/badge.svg?branch=master)](https://coveralls.io/github/GenePeeks/py-rest-orm?branch=master)

Generic Python REST ORM. Inspired by Django. Powered by Requests.

# Installation

**Latest Version**:
```pip install https://github.com/GenePeeks/py-rest-orm.git```

**Stable Build**:
*Coming soon*

# Usage

Unpaginated API
```python
>>> from pyrestorm.models import RestModel

>>> class Post(RestModel):
>>>     url = 'http://jsonplaceholder.typicode.com/posts'

>>>     def __repr__(self):
>>>         return '%s - %s' % (self.id, self.title)

>>> posts = Post.objects.all()
>>> print posts[0]
1 - sunt aut facere repellat provident occaecati excepturi optio reprehenderit
```

Paginated API With Filtering
```python
>>> from pyrestorm.models import RestModel
>>> from pyrestorm.paginators import DjangoRestFrameworkLimitOffsetPaginator

>>> class Gene(RestModel):
>>>     url = 'https://api.genepeeks.com/genes/'
>>>     paginator_class = DjangoRestFrameworkLimitOffsetPaginator

>>>     def __repr__(self):
>>>         return '%s [%s:%s]' % (self.slug, self.start, self.end)

>>> genes = Gene.objects.all()
>>> print genes[0]
RPH3AL [62293:236045]

>>> gene = Gene.objects.get(name='PEX10')
>>> print gene
PEX10 [2336236:2345236]

>>> Gene.objects.get(name__icontains='PEX')
raise Gene.MultipleObjectsReturned

>>> Gene.objects.get(name='PEXCFTR')
raise Gene.DoesNotExist
```