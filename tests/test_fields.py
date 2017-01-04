from datetime import date, datetime
from unittest import TestCase

from pyrestorm.fields import Field, DateField
from pyrestorm import exceptions


class FieldsTestCase(TestCase):
    def test_field_clean(self):
        field = Field()
        self.assertRaises(NotImplementedError, field.clean, 1)

    def test_field_restore(self):
        d = '2016-01-01'
        field = Field()
        self.assertEqual(field.restore(d), d)

    def test_datefield_clean(self):
        d = date(2016, 1, 1)
        field = DateField()
        self.assertEqual(field.clean(d), '2016-01-01')

    def test_datefield_restore(self):
        d = '2016-01-01'
        field = DateField()
        self.assertEqual(field.restore(d), datetime(2016, 1, 1))

    def test_datefield_validate_true(self):
        d = date(2016, 1, 1)
        field = DateField()
        self.assertIsNone(field.validate(d))

    def test_datefield_validate_false(self):
        field = DateField()
        self.assertRaises(exceptions.ValidationError, field.validate, 'tomato')
