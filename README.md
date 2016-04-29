# py-rest-orm
[![Coverage Status](https://coveralls.io/repos/github/GenePeeks/py-rest-orm/badge.svg?branch=master)](https://coveralls.io/github/GenePeeks/py-rest-orm?branch=master)

Generic Python REST ORM. Inspired by Django. Powered by Requests.

# Installation

**Latest Version**:
```pip install https://github.com/GenePeeks/py-rest-orm.git```

**Stable Build**:
*Coming soon*

# Usage

```
>>> from pyrestorm.models import RestModel

>>> class Post(RestModel):
>>>     url = 'http://jsonplaceholder.typicode.com/posts'

>>>     def __repr__(self):
>>>         return '%s - %s' % (self.id, self.title)

>>> posts = Post.objects.all()
>>> print posts[0]
1 - sunt aut facere repellat provident occaecati excepturi optio reprehenderit
```

```
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
```