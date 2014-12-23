from parse_rest.core import ResourceRequestNotFound

from .base import Parse, ParseField


class userStatistics(Parse):
    user = ParseField('userObjectID')
    beacon = ParseField('beaconObjectID')

    def user_gender(self):
        try:
            return self.user.gender
        except ResourceRequestNotFound:
            return 'unknown'

    def user_age_range(self):
        try:
            return self.user.age_range
        except ResourceRequestNotFound:
            return 'unknown'

    def valid(self):
        try:
            self.user.gender
        except ResourceRequestNotFound:
            return False
        else:
            return True

    @classmethod
    def for_beacons(cls, beacons):
        return [s for s in Statistic.Query.filter(beaconObjectID__in=beacons)
                    if s.valid()]


Statistic = userStatistics
