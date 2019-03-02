from marshmallow import Schema, fields


class GetPaymentsSchema(Schema):
    external_id = fields.String()
    patient_id = fields.Integer()
    amount = fields.Integer()


class GetPatientsSchema(Schema):
    external_id = fields.String()
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    middle_name = fields.String()
    date_of_birth = fields.Date()


getPaymentsSchema = GetPaymentsSchema(many=True)
getPatientsSchema = GetPatientsSchema(many=True)
