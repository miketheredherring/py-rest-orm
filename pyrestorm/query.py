from pyrestorm.client import RestClient


class RestQueryset(object):
    _data = None
    _stale = True

    def __init__(self, model, *args, **kwargs):
        self._count = 0
        self._data = []
        self._paginator = model.paginator_class() if hasattr(model, 'paginator_class') else None
        self.model = model
        self.client = RestClient()

    def __iter__(self):
        return iter(self._evaluate())

    def __getitem__(self, value):
        self._evaluate()
        return self._data[value]

    def __len__(self):
        self._evaluate()
        return len(self._data)

    def __repr__(self):
        self._evaluate()
        return str(self)

    def __str__(self):
        return str(self._data)

    def __unicode__(self):
        return unicode(self._data)

    def _fetch(self):
        # Only perform a query if the data is stale
        if self._stale:
            response = self.client.get(self.model.url)
            self._data = [self.model(data=item) for item in response]
            self._count = len(self._data)
            self._stale = False
        return self._data

    def _fetch_pages(self, start, end):
        # Move the paginator to the beginning of the segment of interest
        self._paginator.cursor(start)

        # Only perform a query if the data is stale
        if self._stale:
            # Naive data reset, we can only cache for the current query
            self._data = []
            self._count = 0

            # While we don't have all the data we need, fetch
            self._paginator.cursor(start)
            fetch = True
            while fetch:
                # Retrieve data from the server
                response = self.client.get('%s?%s' % (self.model.url, self._paginator.as_url()))

                # Attempt to grab the size of the dataset from the usual place
                self._paginator.count = response.get('count', None)

                # Count how many record were retrieved in this round
                count = len(response)

                # Extend the dataset with the new records
                self._data.extend([self.model(data=item) for item in response])

                # Increment the number of records we currently have in the queryset
                self._count += count

                # Determine if we need to grab another round of records
                fetch = self._paginator.next(retrieved=count) if end is None else self._count < (end - start)

            # Data is up-to-date
            self._stale = False
        return self._data

    def _evaluate(self, start=0, end=None):
        if self._paginator is not None:
            end = self._paginator.count if end is None else end
            # Check for valid usage
            if end is not None and start >= end:
                raise ValueError('`start` cannot be greater than or equal to `end`')
            elif self._paginator.count is not None and end >= self._paginator.count:
                raise ValueError('`end` cannot be greater than or equal to the maximum number of records')

            return self._fetch_pages(start, end)

        return self._fetch()
