class RestPaginator(object):
    '''Base paginator class which provides method templates.
    '''
    def __init__(self, page_size=20, **kwargs):
        # Maximum number of elements expected to be returned. If None, max will be intelligently determined
        self.max = kwargs.get('max', None)
        # Current location of the cursor in the queryset
        self.position = 0
        # How many records should be retrived per request
        self.page_size = page_size

    def next(self):
        '''Advances the cursor to the next valid location, if available.

        Returns:
            bool: True if successful, otherwise False.
        '''
        raise NotImplementedError

    def prev(self):
        '''Advances the cursor to the previous valid location, if available.

        Returns:
            bool: True if successful, otherwise False.
        '''
        raise NotImplementedError

    def cursor(self, *args, **kwargs):
        '''Moves the cursor to a specified position in the queryset.

        Args:
            position (int): What index of the queryset to seek to?

        Returns:
            bool: True if the cursors postion changed
        '''
        position = getattr(self, 'position', 0)

        # Check for the 'required' position argument, move the cursor if provided
        if len(args) == 1 and args[0] >= 0:
            position = args[0]

        # Determine if the cursor moved, then move it
        cursor_moved = (position == self.position)
        self.position = position

        return cursor_moved

    def set_max(self, maximum):
        '''Sets the maximum range of the paginator.
        '''
        self.max = maximum

    def as_params(self):
        '''Converts attributes needed for URL encoding to **kwargs.

        Returns:
            dict: Key-value pairs for variables of the class instance.
        '''
        return {}


class DjangoRestFrameworkLimitOffsetPaginator(RestPaginator):
    def __init__(self, limit=20, **kwargs):
        # Parameter renaming
        return super(DjangoRestFrameworkLimitOffsetPaginator, self).__init__(page_size=limit, **kwargs)

    # Retrieved is meant to educate the paginator on the amount of results retrieved last request
    def next(self):
        if not self.page_size or not self.max:
            return False
        # If we don't know how many records there are, and we retrieved a full page last request, next could exist
        # Or if advancing doesn't bring us past the known end
        elif self.position + self.page_size <= self.max:
            self.position += self.page_size
            return True
        return False

    # Underflow logic is much simpler since start is a know position
    def prev(self):
        # Can't go any further back than the beginning
        if self.position == 0:
            return False
        # If we will overshoot the beginning, floor to 0 index
        elif self.position - self.page_size <= 0:
            self.position = 0
        # There is definitely enough room to go back
        else:
            self.position -= self.page_size

        return True

    def cursor(self, *args, **kwargs):
        super(DjangoRestFrameworkLimitOffsetPaginator, self).cursor(*args, **kwargs)
        self.page_size = kwargs.get('limit', self.page_size)

    # Extract the number of results from the response
    def set_max(self, response):
        if self.max is None:
            return super(DjangoRestFrameworkLimitOffsetPaginator, self).set_max(response['count'])

    # Dictionary of URL params for pagination
    def as_params(self):
        params = {'offset': unicode(self.position)}
        if self.page_size is not None:
            params['limit'] = unicode(self.page_size)
        return params
