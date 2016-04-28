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