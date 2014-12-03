from .base import Parse, ParseField
from .beacon import Beacon


class merchant(Parse):
    username = ParseField('adminUserName')
    is_superuser = ParseField('superUser', default=False)

    def get_id(self):
        # This method is required by flask-login
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    @property
    def beacons(self):
        if self.is_superuser:
            return Beacon.Query.all()
        else:
            return Beacon.Query.filter(merchantObjectId=self.as_pointer)

    def beacon(self, beacon_id):
        try:
            return self.beacons.filter(objectId=beacon_id)[0]
        except IndexError:
            return None


# Make class camel-case for consistency
Merchant = merchant
