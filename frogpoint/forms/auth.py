from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Optional

from flask_wtf import Form

from ..models.merchant import Merchant


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', validators=[Optional()],
                            default=False)

    def validate_username(self, field):
        if self.user is None:
            raise ValidationError('Wrong username or password')

    def validate_password(self, field):
        if self.user and self.user.adminPass != field.data:
            raise ValidationError('Wrong username or password')

    @property
    def user(self):
        if not hasattr(self, '_user'):
            self._user = Merchant.by_username(self.username.data)
        return self._user
