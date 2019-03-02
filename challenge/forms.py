from wtforms import Form
from wtforms import StringField, ValidationError, IntegerField
from wtforms.validators import Optional


class GetPatientsForm(Form):
    payment_min = IntegerField('payment_min', validators=[Optional()])
    payment_max = IntegerField('payment_max', validators=[Optional()])

    def validate_payment_max(self, value):
        if not self.payment_min.data or not value.data:
            return
        if value.data < self.payment_min.data:
            raise ValidationError('payment_max is less then payment_min.')


class GetPaymentsForm(Form):
    external_id = StringField('external_id')
