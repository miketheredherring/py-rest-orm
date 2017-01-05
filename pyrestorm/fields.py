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
    def configure(self, name):
        '''Makes field knowledgeable of name it is assigned to.
        '''
        pass

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


class TypedField(Field):
    '''Enforces via validate that the value is of a specific type.
    '''
    types = None

    def validate(self, value):
        if isinstance(value, self.types) is False:
            raise ValidationError('`%s` is not of type(s) (%s, )' % (value, self.types))


class IntegerField(TypedField):
    '''Whole number field.
    '''
    types = (int, )


class DateField(TypedField):
    '''Parse ISO timestamps to Python objects.
    '''
    # ISO8601 date format
    date_format = '%Y-%m-%d'
    types = (date, datetime)

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


class DateTimeField(DateField):
    # ISO8601 date format
    date_format = '%Y-%m-%dT%H:%M:%S'


class RelatedField(Field):
    '''Inheritance structure to determine if `Field` is of the related type.
    '''
    pass


class OneToManyField(RelatedField):
    '''Maps detail API routes to existing `RestModel`

    This allows a delaration like the following:
        class Subject:
            class Meta:
                url = 'https://api.genepeeks.com/subjects/'
            genes = RelatedModelField(Gene, route='genes')

    `subject.genes` would hit: https://api.genepeeks.com/subjects/genes/
    '''
    def __init__(self, to, *args, **kwargs):
        self.to = to
        self.url = kwargs.pop('url', None)
        super(OneToManyField, self).__init__(*args, **kwargs)

    def configure(self, parent_class, name):
        '''Makes field knowledgeable of class/name it is assigned to.
        '''
        if self.url is None:
            self.url = name.replace('_', '-')
