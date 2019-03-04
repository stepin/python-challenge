from wtforms import Form, FloatField, StringField, ValidationError
from wtforms.validators import Optional


class GetPatientsForm(Form):
    payment_min = FloatField('payment_min', validators=[Optional()])
    payment_max = FloatField('payment_max', validators=[Optional()])

    def validate_payment_max(self, value):
        if not self.payment_min.data or not value.data:
            return
        if value.data < self.payment_min.data:
            raise ValidationError('payment_max is less then payment_min.')


class GetPaymentsForm(Form):
    external_id = StringField('external_id')
