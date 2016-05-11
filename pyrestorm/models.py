import six

from pyrestorm.client import RestClient
from pyrestorm.exceptions import orm as orm_exceptions
from pyrestorm.manager import RestOrmManager


class RestModelBase(type):
    # Called when class is imported got guarantee proper setup of child classes to parent
    def __new__(cls, name, bases, attrs):
        # Call to super
        super_new = super(RestModelBase, cls).__new__

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, RestModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the current class
        new_class = super_new(cls, name, bases, {'__module__': attrs.pop('__module__')})
        new_class._meta = attrs.pop('Meta', None)

        # Clean the incoming data, URL should not contain trailing slash for proper assembly
        new_class._meta.url = new_class._meta.url.rstrip('/')
        # Parse authentication if it is present
        if hasattr(new_class._meta, 'token'):
            if not hasattr(new_class._meta, 'token_prefix'):
                new_class._meta.token_prefix = 'Token'

        # Django attributes(Doesn't hurt to have them)
        new_class._meta.model_name = new_class.__name__
        new_class._meta.app_label = new_class.__module__.split('.')[-1]

        # Check if user is overriding URL scheme
        if not hasattr(new_class._meta, 'slug_field'):
            new_class._meta.slug_field = 'id'

        # Instantiate the manager instance
        new_class.objects = new_class.objects()

        # Make links to children if they ask for it, shamelessly stolen from Django
        for attr in [attr for attr in dir(new_class) if not callable(attr) and not attr.startswith('__')]:
            if hasattr(getattr(new_class, attr), 'contribute_to_class'):
                getattr(new_class, attr).contribute_to_class(new_class)

        # Defines shortcut for exceptions
        new_class.DoesNotExist = type('DoesNotExist', (orm_exceptions.DoesNotExist, ), {})
        new_class.MultipleObjectsReturned = type('MultipleObjectsReturned', (orm_exceptions.MultipleObjectsReturned, ), {})

        return new_class


class RestModel(six.with_metaclass(RestModelBase)):
    # Bind the JSON data from a response to a new instance of the model
    def __init__(self, *args, **kwargs):
        self._data = kwargs.pop('data', {})
        super(RestModel, self).__init__()

        data_to_bind = self._data
        # Check for arguments the user provided
        if bool(self._data) is False:
            data_to_bind = kwargs

        # Bind data to the model
        self._bind_data(self, data_to_bind)

    # Manager to act like Django ORM
    objects = RestOrmManager

    @classmethod
    def get_client(cls):
        return RestClient(
            token=getattr(cls._meta, 'token', None),
            authorization_header=getattr(cls._meta, 'token_prefix', None)
        )

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

    # Returns the URL to this resource
    def get_absolute_url(self):
        return '/'.join([self._meta.url, unicode(getattr(self, self._meta.slug_field)), ''])

    # Does not save nested keys
    def save(self, raise_exception=False, **kwargs):
        # Difference between the original model and new one
        diff = {}

        # For all of the top level keys
        for key, value in self.__dict__.iteritems():
            # Do not worry about nested values
            if isinstance(value, dict):
                continue

            if self._data.get(key, '__SENTINEL__') != value:
                diff[key] = value

        # Perform a PATCH only if there are difference
        if diff:
            client = self.get_client()

            url = self._meta.url
            method = client.post
            # Check if this is an update or a new instance
            if bool(self._data) is True:
                url = self.get_absolute_url()
                method = client.patch

            # Update the local model on success
            self._data = method(url, diff)
            self._bind_data(self, self._data)
