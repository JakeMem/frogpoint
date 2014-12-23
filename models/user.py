from parse_rest.connection import API_ROOT

from .base import Parse, ParseField


class User(Parse):
    birthday = ParseField('Birthday')
    first_name = ParseField('FirstName')
    last_name = ParseField('LastName')
    gender = ParseField('Gender')
    age_range = ParseField('ageRange')

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
