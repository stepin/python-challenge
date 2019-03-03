import uuid

from flask import Blueprint, jsonify, request
from sqlalchemy.sql import func

from challenge.json_schemas import getPaymentsSchema, getPatientsSchema, postPaymentsSchema, postPatientsSchema
from challenge.models import db, Patient
from challenge.forms import GetPaymentsForm, GetPatientsForm
from challenge.models import Payment
from challenge.upsert import upsert_patients, upsert_payments

api = Blueprint('api', __name__)


def _sql_tuple_to_patients(patient_tuple):
    patient = patient_tuple[0]
    total_amount = patient_tuple[1]
    patient.total_amount = total_amount
    return patient


def _get_patients(payment_min, payment_max):
    stmt = db.session.query(
        Payment.patient_id,
        func.sum(Payment.amount).label('total_amount')
    )
    if payment_min:
        stmt = stmt.filter(Payment.amount >= payment_min)
    if payment_max:
        stmt = stmt.filter(Payment.amount <= payment_max)
    stmt = stmt.group_by(Payment.patient_id).subquery()

    query = db.session.query(Patient, func.ifnull(stmt.c.total_amount, 0.0)). \
        outerjoin(stmt, Patient.id == stmt.c.patient_id)

    patients_tuple = query.all()
    patients_list = map(_sql_tuple_to_patients, patients_tuple)
    patients_json = getPatientsSchema.dump(patients_list)
    return patients_json


def patients_get():
    form = GetPatientsForm(request.args)
    if not form.validate():
        return f"Submitted params are invalid: {form.errors}", 422

    patients_json = _get_patients(form.data["payment_min"], form.data["payment_max"])
    return str(patients_json)


def _update_patients(json, sync_id):
    patients = postPatientsSchema.load(json)
    upsert_patients(patients, sync_id)


def _delete_old_patients(sync_id):
    db.session.query(Patient).filter(Patient.sync_id != sync_id).delete(synchronize_session=False)


def patients_post():
    content = request.json
    sync_id = _create_sync_id()

    _update_patients(content, sync_id)
    _delete_old_patients(sync_id)
    db.session.commit()

    return jsonify({'status': 'OK'})


def _get_patient_id(patient_external_id):
    patient = db.session.query(Patient) \
        .filter(Patient.external_id == patient_external_id) \
        .first()
    if not patient:
        return None
    return patient.id


def _get_payments(patient_external_id):
    query = db.session.query(Payment)
    if patient_external_id:
        patient_id = _get_patient_id(patient_external_id)
        if not patient_id:
            return jsonify([])
        query = query.filter(Payment.patient_id == patient_id)

    payments_list = query.all()
    payments_json = getPaymentsSchema.dump(payments_list)
    return str(payments_json)


def payments_get():
    form = GetPaymentsForm(request.args)
    if not form.validate():
        return f"Submitted params are invalid: {form.errors}", 422

    payments_json = _get_payments(form.data["external_id"])
    return payments_json


def _update_payments(json, sync_id):
    payments = postPaymentsSchema.load(json)
    upsert_payments(payments, sync_id)


def _delete_old_payments(sync_id):
    db.session.query(Payment).filter(Payment.sync_id != sync_id).delete(synchronize_session=False)


def _create_sync_id():
    return uuid.uuid4().hex


def payments_post():
    content = request.json
    sync_id = _create_sync_id()

    _update_payments(content, sync_id)
    _delete_old_payments(sync_id)
    db.session.commit()

    return jsonify({'status': 'OK'})


@api.route('/patients', methods=['POST', 'GET'])
def patients():
    method = patients_post if request.method == 'POST' else patients_get
    return method()


@api.route('/payments', methods=['POST', 'GET'])
def payments():
    method = payments_post if request.method == 'POST' else payments_get
    return method()
