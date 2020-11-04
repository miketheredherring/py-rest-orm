import copy
import six

from pyrestorm.client import RestClient
from pyrestorm.fields import Field, RelatedField
from pyrestorm.exceptions import orm as orm_exceptions
from pyrestorm.query import RestQueryset
from pyrestorm.manager import RestOrmManager

primitives = [int, bytes, str, bool, type(None)]
non_object_types = [dict, list, tuple]

SENTINEL = '__SENTINEL__'


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
        new_class = super_new(cls, name, bases, attrs)
        new_class._meta = attrs.pop('Meta', None)

        # Check if user is overriding URL scheme
        if not hasattr(new_class._meta, 'slug_field'):
            new_class._meta.slug_field = 'id'

        # Binds `Field` instances to the meta class for validation
        new_class._meta.fields = {}
        new_class._meta.related_fields = {}
        for name in list(attrs.keys()):
            if isinstance(attrs[name], Field):
                new_class._meta.fields[name] = attrs.pop(name)
                # Keep track of `RelatedFields` specially
                if isinstance(new_class._meta.fields[name], RelatedField):
                    new_class._meta.related_fields[name] = new_class._meta.fields[name]
                    new_class._meta.related_fields[name].configure(new_class, name)

        # Clean the incoming data, URL should not contain trailing slash for proper assembly
        new_class._meta.url = new_class._meta.url.rstrip('/')

        # URL forming with append slash set to default True
        new_class._meta.append_slash = getattr(new_class._meta, 'append_slash', True)

        # Parse authentication if it is present
        if hasattr(new_class._meta, 'token'):
            if not hasattr(new_class._meta, 'token_prefix'):
                new_class._meta.token_prefix = 'Token'

        # Django attributes(Doesn't hurt to have them)
        new_class._meta.model_name = new_class.__name__
        new_class._meta.app_label = new_class.__module__.split('.')[-1]

        # Instantiate the manager instance
        new_class.objects = new_class.objects()

        # Make links to children if they ask for it, shamelessly stolen from Django
        for attr in [attr for attr in dir(new_class) if not callable(attr) and not attr.startswith('__')]:
            if hasattr(getattr(new_class, attr), 'contribute_to_class'):
                getattr(new_class, attr).contribute_to_class(new_class)

        # Defines shortcut for exceptions specific to this model type
        new_class.DoesNotExist = type('DoesNotExist', (orm_exceptions.DoesNotExist, ), {})
        new_class.MultipleObjectsReturned = type('MultipleObjectsReturned', (orm_exceptions.MultipleObjectsReturned, ), {})

        return new_class


class RestModel(six.with_metaclass(RestModelBase)):
    # Bind the JSON data from a response to a new instance of the model
    def __init__(self, *args, **kwargs):
        self._data = kwargs.pop('_json', {})
        super(RestModel, self).__init__()

        data_to_bind = self._data
        # Check for arguments the user provided
        if bool(self._data) is False:
            data_to_bind = kwargs

        # Bind data to the model
        self._bind_data(self, data_to_bind)

        # Bind to the name of the field a `RestQueryset` of the correct type
        for name, field in self._meta.related_fields.items():
            # Don't rebind data which already exists
            if hasattr(self, self._meta.slug_field) is True:
                setattr(
                    self,
                    name,
                    field.to.objects.get_queryset_class(
                        url='/'.join([self.get_absolute_url().rstrip('/'), field.url, ''])
                    )
                )

    # Manager to act like Django ORM
    objects = RestOrmManager

    @property
    def slug(self):
        return getattr(self, self._meta.slug_field)

    #  DJANGO COMPATABILITY

    def serializable_value(self, value):
        '''All JSON is of serializable types, thus just return the value
        '''
        return getattr(self, value)

    # Returns a new client
    @classmethod
    def get_client(cls):
        return RestClient(
            token=getattr(cls._meta, 'token', None),
            authorization_header=getattr(cls._meta, 'token_prefix', None)
        )

    # Bind the JSON data to the new instance
    @staticmethod
    def _bind_data(obj, data):
        for key, val in data.items():
            # Bind the data to the next level if need be
            if isinstance(val, dict):
                # Create the class if need be, otherwise do nothing
                setattr(obj, key, type(str(key.title()), (), {})) if not hasattr(obj, key) else None
                attr = getattr(obj, key)
                RestModel._bind_data(attr, val)
            else:
                restore_value = copy.deepcopy(val)
                if key in getattr(getattr(obj, '_meta', None), 'fields', {}):
                    restore_value = obj._meta.fields[key].restore(restore_value)
                setattr(obj, key, restore_value)

    @staticmethod
    def _get_reference_data(ref, idx):
        ref_type = type(ref)
        ret = ref
        if ref_type == list:
            try:
                ret = ref[idx]
            except ValueError:
                ret = SENTINEL
        elif ref_type == dict:
            ret = ref.get(idx, SENTINEL)

        return ret

    def _serialize_data(self, obj, ref):
        '''Converts the local Python objects into a JSON structure.

        There are 3 cases we need to handle in this recursive function:
            1. Primitives: Should be serialized to JSON as-is
            2. List: Iterate over all elements and call _serialize_data on each
            3. Dictionary/Object: Recursively call _serialize_data

        Arguments:
            obj - The current attribute on the model which we are comparing
                against the previous state for changes.
            ref - Reference data stored on the `RestModel` for the attribute
                layer currently being looked at. Used for saving since a
                HTTP PATCH is used for updates, where we only send the delta.

        Returns:
            dict - Dictionary diff for the models current state and the last load.
        '''
        local_diff = {}

        # Get the `dict` representation of the `object` to combine cases
        if type(obj) not in (primitives + non_object_types):
            obj = obj.__dict__

        # Check each value in the `dict` for changes
        for key, value in obj.items():
            # 0. Private variables: SKIP
            # Escape early if nothing has changed
            if key.startswith('_') or self._get_reference_data(ref, key) == value:
                continue

            # Check if the value can be cleaned
            cleaned_value = value

            # Serializing of a `RestQueryset` is currently unsuppored since there
            # is no public way to create one without querying, which means the data
            # already exists on the server.
            if isinstance(value, RestQueryset):
                return local_diff

            # Determine what type the current `value` is to process one of the three cases
            value_type = type(value)

            # 1. Primitives
            if value_type in primitives:
                # If the value of the field is not what we've seen before, add it to the diff
                if ref != cleaned_value:
                    local_diff[key] = cleaned_value
            # 2/3. Objects
            else:
                # 2. Lists
                if value_type == list:
                    # Process each idex of the `list`
                    local_diff[key] = []
                    for idx, inner_value in enumerate(cleaned_value):
                        if type(inner_value) in primitives:
                            local_diff[key].append(inner_value)
                        else:
                            local_diff[key].append(self._serialize_data(inner_value, self._get_reference_data(ref, idx)))
                # 3. Object/Dictionary
                else:
                    new_ref = self._get_reference_data(ref, key)
                    _data = self._serialize_data(cleaned_value, new_ref)
                    if not _data and value_type not in (primitives + non_object_types):
                        continue
                    local_diff[key] = _data

        return local_diff

    # Returns the base URL for this resource type
    @classmethod
    def get_base_url(cls, bits=[]):
        # Assemble from the base url
        url_bits = [cls._meta.url, ]
        url_bits.extend(bits)

        # Handle trailing slash if requested
        if cls._meta.append_slash is True:
            url_bits.append('')

        return '/'.join(url_bits)

    # Returns the URL to this resource
    def get_absolute_url(self):
        return self.get_base_url(bits=[str(getattr(self, self._meta.slug_field, '')), ])

    # Does not save nested keys
    def save(self, raise_exception=False, **kwargs):
        # Difference between the original model and new one
        diff = self._serialize_data(self, self._data)

        # Perform a PATCH only if there are difference
        if diff:
            client = self.get_client()

            url = self.get_base_url()
            method = client.post
            # Check if this is an update or a new instance
            if bool(self._data) is True:
                url = self.get_absolute_url()
                method = client.patch

            # Update the local model on success
            self._data = method(url, diff)
            self._bind_data(self, self._data)
