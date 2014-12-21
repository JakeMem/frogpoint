from .base import Parse, ParseField
from .user_statistics import Statistic


class Beacons(Parse):
    alias = ParseField('aliasName', default='')
    coupon = ParseField('couponsObjectID')

    PROXIMITY_CHOICES = [
        (1, 'Immediate'),
        (2, 'Near'),
        (3, 'Far')
    ]

    @property
    def action(self):
        if self.coupon:
            return self.coupon.friendly_type()

    @property
    def statistics(self):
        return Statistic.Query.filter(beaconObjectID=self)


# Make singular class for consistency
Beacon = Beacons
