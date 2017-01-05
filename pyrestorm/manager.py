from pyrestorm.query import RestQueryset


class RestOrmManager(object):
    def __init__(self, queryset_class=None, **kwargs):
        super(RestOrmManager, self).__init__(**kwargs)
        self.queryset_class = queryset_class or RestQueryset

    # Ensure the objects is only available at the class level
    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError('`RestOrmManager` isn\'t accessible via `%s` instances' % cls.__name__)
        return self

    def __getattr__(self, value, *args, **kwargs):
        # Make sure its not a private method
        if not value.startswith('_') and hasattr(self.queryset_class, value):
            _queryset = self.get_queryset_class()
            return getattr(_queryset, value)

    def get_queryset_class(self, *args, **kwargs):
        return self.queryset_class(self.model, *args, **kwargs)

    # Since the OrmManager instance is instantiated on the RestModel, this allows us to know the parent class
    def contribute_to_class(self, cls):
        self.model = cls
