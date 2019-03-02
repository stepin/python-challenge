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
    total_amount = fields.Integer()


class PostPaymentsSchema(Schema):
    externalId = fields.String(attribute="external_id")
    patientId = fields.Integer(attribute="patient_id")
    amount = fields.Integer()


class PostPatientsSchema(Schema):
    externalId = fields.String(attribute="external_id")
    firstName = fields.String(attribute="first_name")
    lastName = fields.String(attribute="last_name")
    dateOfBirth = fields.Date(attribute="date_of_birth")


getPaymentsSchema = GetPaymentsSchema(many=True)
getPatientsSchema = GetPatientsSchema(many=True)
postPaymentsSchema = PostPaymentsSchema(many=True)
postPatientsSchema = PostPatientsSchema(many=True)
