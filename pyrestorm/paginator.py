class RestPaginator(object):
    def __init__(self, page_size=20, **kwargs):
        self.count = kwargs.get('count', None)
        self.position = 0
        self.page_size = page_size

    def next(self):
        raise NotImplementedError

    def prev(self):
        raise NotImplementedError

    def cursor(self, *args):
        position = 0
        # Check for the required position argument
        if len(args) == 1:
            position = args[0]
            # raise ValueError('`position` argument must be specified for the cursor')
        self.position = position


class DjangoRestFrameworkLimitOffsetPaginator(RestPaginator):
    def __init__(self, limit=20, **kwargs):
        return super(DjangoRestFrameworkLimitOffsetPaginator, self).__init__(page_size=limit, **kwargs)

    def next(self, retrieved=None):
        ret = True
        if (self.count is None and (retrieved == self.page_size or retrieved is None)) or (self.position + self.page_size <= self.count):
            self.position += self.page_size
        else:
            ret = False
        return ret

    def prev(self):
        ret = True
        if self.position >= self.page_size:
            self.position -= self.page_size
        elif self.position - self.page_size <= 0 and self.position - self.page_size > -self.page_size:
            self.position = 0
        else:
            ret = False

        return ret

    def as_url(self):
        return 'limit=%s&offset=%s' % (self.page_size, self.position)
