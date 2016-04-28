from pyrestorm.client import RestClient
from pyrestorm.exceptions import orm as orm_exceptions


class RestOrmManager(object):
    # Ensure the objects is only available at the class level
    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError('`RestOrmManager` isn\'t accessible via `%s` instances' % cls.__name__)
        return self

    def contribute_to_class(self, cls):
        self.model = cls

    def all(self, *args, **kwargs):
        response = self.model.client.get(self.model.url)
        items = []
        for item in response:
            items.append(self.model(data=item))

        return items


class RestModel(object):
    # Root URL for REST model
    url = None

    def __new__(cls, *args, **kwargs):
        ret = super(RestModel, cls).__new__(cls, *args, **kwargs)

        # Make sure the proper fields are overriden
        if cls.url is None:
            raise NotImplementedError('`url` must be declared when inheriting `RestModel`')

        # Create a new client
        cls.client = RestClient()

        # Make links to children if they ask for it, shamelessly stolen from Django
        for attr in [attr for attr in dir(cls) if not callable(attr) and not attr.startswith('__')]:
            if hasattr(getattr(cls, attr), 'contribute_to_class'):
                getattr(cls, attr).contribute_to_class(cls)

        return ret

    def __init__(self, *args, **kwargs):
        data = kwargs.pop('data', {})
        ret = super(RestModel, self).__init__(*args, **kwargs)

        # Bind data to the model
        self._bind_data(self, data)

        return ret

    # Manager to act like Django ORM
    objects = RestOrmManager()

    # Defines shortcut for exceptions
    DoesNotExist = orm_exceptions.DoesNotExist

    # Bind the JSON data to the new instance
    @staticmethod
    def _bind_data(obj, data):
        for key, val in data.iteritems():
            # Bind the data to the next level if need be
            if isinstance(val, dict):
                # Create the class if need be, otherwise do nothing
                setattr(obj, key, type(key.title(), (), {})) if not hasattr(obj, key) else None
                attr = getattr(obj, key)
                RestModel._bind_data(attr, val)
            else:
                setattr(obj, key, val)
