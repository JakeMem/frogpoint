from wtforms import BooleanField, StringField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, URL, Optional

from flask_wtf import Form

from .fields import InlineRadioField
from ..models.beacon import Beacon
from ..models.coupon import Coupon


class CouponForm(Form):
    type = SelectField('Type', choices=Coupon.TYPES_CHOICES,
                       validators=[DataRequired()])
    proximity = InlineRadioField('Proximity', choices=Beacon.PROXIMITY_CHOICES,
                                 coerce=int)
    enabled = BooleanField('Enabled?')

    # type=message
    message_text = StringField('Message', validators=[Length(max=80),
                                                      Optional()])

    # type=image
    image_url = StringField('Image URL', validators=[URL(), Optional()])

    # type=url
    url_url = StringField('URL', validators=[URL(), Optional()])

    # type=timer
    timer_title = StringField('Offer Title', validators=[Optional()])
    timer_description = StringField('Offer Description',
                                    validators=[Optional()])
    timer_minutes = SelectField('Time', choices=Coupon.TIME_CHOICES,
                                coerce=int, validators=[Optional()])

    # type=voucher
    voucher_logo_url = StringField('Logo URL', validators=[URL(), Optional()])
    voucher_title = StringField('Offer Title', validators=[Optional()])
    voucher_description = StringField('Offer Description',
                                      validators=[Optional()])
    voucher_template_id = SelectField('Template',
                                      choices=Coupon.TEMPLATE_CHOICES,
                                      validators=[Optional()])
    voucher_valid_from = DateTimeField('Valid from', validators=[Optional()],
                                       format='%Y-%m-%d %H:%M')
    voucher_valid_to = DateTimeField('Valid to', validators=[Optional()],
                                     format='%Y-%m-%d %H:%M')

    def __init__(self, beacon, *args, **kwargs):
        self.beacon = beacon
        self.coupon = beacon.coupon or Coupon()
        kwargs.setdefault('data', {})
        kwargs['data']['proximity'] = beacon.proximity
        kwargs['data']['type'] = self.coupon.type or Coupon.DEFAULT_TYPE
        kwargs['data']['enabled'] = self.coupon.enabled or False

        if self.coupon.type:
            func_name = 'initial_data_{0}'.format(self.coupon.type)
            coupon_data = getattr(self, func_name)(self.coupon)
            kwargs['data'].update(coupon_data)
        super(CouponForm, self).__init__(*args, **kwargs)

    def save(self):
        coupon = self.coupon
        coupon.type = self.type.data
        load_data_func = getattr(self, 'save_{0}'.format(self.type.data))
        load_data_func(coupon)
        coupon.save()

        beacon = self.beacon
        beacon.proximity = self.proximity.data
        beacon.coupon = coupon
        beacon.save()

        return coupon

    def save_message(self, coupon):
        coupon.message_text = self.message_text.data

    def save_image(self, coupon):
        coupon.image_url = self.image_url.data

    def save_url(self, coupon):
        coupon.url_url = self.url_url.data

    def save_timer(self, coupon):
        coupon.timer_title = self.timer_title.data
        coupon.timer_description = self.timer_description.data
        coupon.timer_minutes = self.timer_minutes.data

    def save_coupon(self, coupon):
        coupon.voucher_logo_url = self.voucher_logo_url.data
        coupon.voucher_title = self.voucher_title.data
        coupon.voucher_description = self.voucher_description.data
        coupon.voucher_valid_from = self.voucher_valid_from.data
        coupon.voucher_valid_to = self.voucher_valid_to.data
        coupon.set_template(self.voucher_template_id.data)

    def initial_data_message(self, coupon):
        return {'message_text': coupon.message_text}

    def initial_data_image(self, coupon):
        return {'image_url': coupon.image_url}

    def initial_data_url(self, coupon):
        return {'url_url': coupon.url_url}

    def initial_data_timer(self, coupon):
        return {
            'timer_title': coupon.timer_title,
            'timer_description': coupon.timer_description,
            'timer_minutes': coupon.timer_minutes
        }

    def initial_data_coupon(self, coupon):
        return {
            'voucher_logo_url': coupon.voucher_logo_url,
            'voucher_title': coupon.voucher_title,
            'voucher_description': coupon.voucher_description,
            'voucher_valid_from': coupon.voucher_valid_from,
            'voucher_valid_to': coupon.voucher_valid_to,
            'voucher_template_id': coupon.voucher_template_id
        }

    def current_type(self):
        if self.is_submitted():
            return self.type.data
        elif self.coupon:
            return self.coupon.type
        else:
            return Coupon.DEFAULT_TYPE
