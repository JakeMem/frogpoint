from wtforms import StringField
from wtforms.validators import DataRequired

from flask_wtf import Form


class AliasForm(Form):
    alias = StringField('Alias', validators=[DataRequired()])

    def __init__(self, beacon, *args, **kwargs):
        self.beacon = beacon
        kwargs['obj'] = beacon
        super(AliasForm, self).__init__(*args, **kwargs)

    def save(self):
        self.beacon.alias = self.alias.data
        self.beacon.save()
        return self.beacon
