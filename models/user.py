from datetime import datetime

from parse_rest.connection import API_ROOT

from .base import Parse, ParseField


class User(Parse):
    birthday = ParseField('Birthday')
    first_name = ParseField('FirstName')
    last_name = ParseField('LastName')
    gender = ParseField('Gender')

    ENDPOINT_ROOT = '/'.join([API_ROOT, 'users'])
    AGE_RANGES = (
        (14, 17),
        (18, 21),
        (21, 30),
        (31, 40),
        (41, 50),
        (51, 60),
    )

    @property
    def is_male(self):
        return self.gender == 'male'

    @property
    def age_range(self):
        age = self.age()
        if age:
            if age <= 13:
                return '<13'
            if age > 60:
                return '61+'
            for age_range in self.AGE_RANGES:
                if age >= age_range[0] and age < age_range[1]:
                    return '{0}-{1}'.format(*age_range)
        return 'unknown'

    def age(self):
        age = getattr(self, '_age', None)
        if age is None:
            if self.birthday:
                date = datetime.strptime(self.birthday, '%m/%d/%Y')
                delta = (datetime.now() - date).days
                age = int(delta / 365) + (1 if delta % 365 > 0 else 0)
            setattr(self, '_age', None)
        return age
