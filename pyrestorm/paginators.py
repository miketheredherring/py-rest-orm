class RestPaginator(object):
    '''
    Base paginator class which provides method templates.
    '''
    def __init__(self, page_size=20, **kwargs):
        # Maximum number of elements expected to be returned. If None, max will be intelligently determined
        self.max = kwargs.get('max', None)
        # Current location of the cursor in the queryset
        self.position = 0
        # How many records should be retrived per request
        self.page_size = page_size

    # Advances the cursor to the correct next location, if available, and returns True if successful, otherwise False
    def next(self):
        raise NotImplementedError

    # Advances the cursor to the correct prevous location, if available, and returns True if successful, otherwise False
    def prev(self):
        raise NotImplementedError

    # Moves the cursor to a specified position in the queryset
    def cursor(self, *args, **kwargs):
        position = 0
        # Check for the 'required' position argument
        if len(args) == 1 and args[0] >= 0:
            position = args[0]

        # Move the cursor
        self.position = position


class DjangoRestFrameworkLimitOffsetPaginator(RestPaginator):
    def __init__(self, limit=20, **kwargs):
        # Parameter renaming
        return super(DjangoRestFrameworkLimitOffsetPaginator, self).__init__(page_size=limit, **kwargs)

    # Retrieved is meant to educate the paginator on the amunt of results retrieved last request
    def next(self, retrieved=None):
        ret = True
        # If we don't know how many records there are, and we retrieved a full page last request, next could exist
        # Or if advancing doesn't bring us past the known end
        if (self.max is None and (retrieved is None or retrieved == self.page_size)) or \
           (self.page_size is not None and self.position + self.page_size <= self.max):
            self.position += self.page_size
        # We can't move
        else:
            ret = False
        return ret

    # Underflow logic is much simpler since start is a know position
    def prev(self):
        ret = True
        # If we are at the beginning and cant move
        if self.position == 0:
            ret = False
        # If we will overshoot the beginning, floor to 0 index
        elif self.position - self.page_size <= 0:
            self.position = 0
        # There is definitely enough room to go back
        else:
            self.position -= self.page_size

        return ret

    def cursor(self, *args, **kwargs):
        super(DjangoRestFrameworkLimitOffsetPaginator, self).cursor(*args, **kwargs)
        self.page_size = kwargs.get('limit', self.page_size)

    # Dictionary of URL params for pagination
    def as_params(self):
        params = {'offset': unicode(self.position)}
        if self.page_size is not None:
            params['limit'] = unicode(self.page_size)
        return params

    # Turn the data structure into a url
    def as_url(self):
        params = self.as_params()
        return 'limit=%s&offset=%s' % (params['limit'], params['offset'])
