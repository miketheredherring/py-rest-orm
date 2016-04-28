from pyrestorm.client import RestClient


class RestQueryset(object):
    _data = None
    _stale = True

    def __init__(self, model, *args, **kwargs):
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

    def _evaluate(self):
        # Only perform a query if the data is stale
        if self._stale:
            response = self.client.get(self.model.url)
            self._data = [self.model(data=item) for item in response]
            self._stale = False
        return self._data
