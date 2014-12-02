import six

from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.datatypes import Object, ObjectMetaclass


class ParseField(object):
    def __init__(self, parse_name=None, default=None):
        self.parse_name = parse_name
        self.default = default

    def contribute_to_class(self, cls, name):
        self.name = name
        self.parse_name = self.parse_name or name
        setattr(cls, name, self)
        setattr(cls, 'by_{0}'.format(name), classmethod(
            lambda klass, value: klass.get_or_none(**{
                self.parse_name: value
            })
        ))

    def __get__(self, instance, type=None):
        try:
            return getattr(instance, self.parse_name)
        except (AttributeError, QueryResourceDoesNotExist):
            return self.default

    def __set__(self, instance, value):
        setattr(instance, self.parse_name, value)


class ParseMetaclass(ObjectMetaclass):
    def __new__(cls, name, bases, attrs):
        new_class = super(ParseMetaclass, cls).__new__(cls, name, bases, {
            '__module__': attrs.pop('__module__'),
            '_fields': {},
        })

        for name, attr in attrs.items():
            if hasattr(attr, 'contribute_to_class'):
                new_class._fields[name] = attr
                attr.contribute_to_class(new_class, name)
            else:
                setattr(new_class, name, attr)

        # Fields from parents
        for parent in bases:
            if not hasattr(parent, '_fields'):
                continue
            for name, attr in parent._fields.items():
                if hasattr(attr, 'contribute_to_class'):
                    if name not in attrs:
                        new_class._fields[name] = attr
                        attr.contribute_to_class(new_class, name)
                else:
                    setattr(new_class, name, attr)

        return new_class


class Parse(six.with_metaclass(ParseMetaclass, Object)):
    id = ParseField('objectId')

    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            return cls.Query.get(**kwargs)
        except QueryResourceDoesNotExist:
            return None
