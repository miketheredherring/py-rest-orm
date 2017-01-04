from datetime import date, datetime

from pyrestorm.exceptions import ValidationError


class Field(object):
    '''Validates and castes incoming data to a desired type.

    When loading models this allows the incoming API data
    to be parsed to certain data types or classes, in order
    to prevent iteration and manual forming of the data.

    Additionally acts as a protection for writing back to APIs
    by validating the data being sent back is of the right type,
    which can be caught without sending a request.
    '''
    def clean(self, value):
        '''Prepares the value for saving.

        Inverse of restore.

        Returns:
            type: Internal representation of the field
        '''
        self.validate(value)
        return value

    def restore(self, value):
        '''Parses data from internal representation to a data structure.

        Inverse of clean.

        Returns:
            type: Rendered version of the field
        '''
        return value

    def validate(self, value):
        '''Does the data bound to this field meet specified criteria?

        Returns:
            bool: True if successful, otherwise False.
        '''
        raise NotImplementedError


class DateField(Field):
    # ISO8601 date format
    date_format = '%Y-%m-%d'
    '''Parse ISO timestamps to Python objects.
    '''
    def __init__(self, *args, **kwargs):
        '''Allows custom date format for parsing and rendering.
        '''
        self.date_format = kwargs.pop('format', self.date_format)
        super(DateField, self).__init__(*args, **kwargs)

    def clean(self, value):
        '''Converts `Date` to string type.
        '''
        value = super(DateField, self).clean(value)
        return value.strftime(self.date_format)

    def restore(self, value):
        '''Converts string type to `Date`.
        '''
        return datetime.strptime(value, self.date_format)

    def validate(self, value):
        '''Ensures value is either `Date`/`DateTime` instance.
        '''
        if isinstance(value, (date, datetime)) is False:
            raise ValidationError('Unable to parse datetime object')


class DateTimeField(DateField):
    # ISO8601 date format
    date_format = '%Y-%m-%dT%H:%M:%S'
