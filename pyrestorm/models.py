import six

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

        # Django attributes(Doesn't hurt to have them)
        new_class._meta.model_name = new_class.__name__
        new_class._meta.app_label = new_class.__module__.split('.')[-1]

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
        data = kwargs.pop('data', {})
        super(RestModel, self).__init__()

        # Bind data to the model
        self._bind_data(self, data)

    # Manager to act like Django ORM
    objects = RestOrmManager

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
