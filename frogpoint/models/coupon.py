from .base import Parse, ParseField


class coupons(Parse):
    type = ParseField('offerType')
    enabled = ParseField('active', default=False)

    # These values are used when type is "message"
    message_text = ParseField('offerDescription', default='')

    # These values are used when type is "image"
    image_url = ParseField('imageURL', default='')

    # These values are used when type is "timer"
    timer_title = ParseField('offerTitle', default='')
    timer_description = ParseField('offerDescription', default='')
    timer_minutes = ParseField('timeLimitMinutes', default=0)

    # These values are used when type is "url"
    url_url = ParseField('offerDescription', default='')

    # These values are used when type is "coupon"
    voucher_logo_url = ParseField('logoURL', default='')
    voucher_title = ParseField('offerTitle', default='')
    voucher_description = ParseField('offerDescription', default='')
    voucher_template_name = ParseField('template', default='')
    voucher_template_id = ParseField('templateID', default='')
    voucher_valid_from = ParseField('validFrom')
    voucher_valid_to = ParseField('validTo')

    DEFAULT_TYPE = 'message'

    TYPES_CHOICES = (
        ('message', 'Message'),
        ('image', 'Image'),
        ('url', 'URL'),
        ('timer', 'Timer'),
        ('coupon', 'Voucher'),
    )

    TIME_CHOICES = [(val, val) for val in range(5, 65, 5)]

    TEMPLATE_CHOICES = [
        ('5097853651255296', 'Generic Coffee'),
        ('5736946529730560', 'Generic Music'),
        ('4866372093870080', 'Generic Fashio'),
        ('5665573232967680', 'Fashion'),
        ('127808001', 'Music'),
        ('5678827367825408', 'Coffee'),
        ('118408001', 'Garden'),
    ]

    TEMPLATE_NAMES = [
        ('5097853651255296', 'Generic_coffee'),
        ('5736946529730560', 'Generic_music'),
        ('4866372093870080', 'Generic_fashio'),
        ('5665573232967680', 'Fashion'),
        ('127808001', 'Music'),
        ('5678827367825408', 'Coffee'),
        ('118408001', 'Garden'),
    ]

    def friendly_type(self):
        return dict(self.TYPES_CHOICES).get(self.type, self.type)

    def set_template(self, template_id):
        self.voucher_template_id = template_id
        self.voucher_template_name = dict(self.TEMPLATE_NAMES).get(template_id)


# Make class camel-case for consistency
Coupon = coupons
