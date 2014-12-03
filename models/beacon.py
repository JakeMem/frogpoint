from .base import Parse, ParseField


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


# Make singular class for consistency
Beacon = Beacons
