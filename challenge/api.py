from flask import Blueprint, jsonify, request
from functools import reduce

from challenge.json_schemas import getPaymentsSchema
from challenge.models import db
from challenge.forms import GetPaymentsForm, GetPatientsForm
from challenge.models import Payment

api = Blueprint('api', __name__)


def patients_get():
    form = GetPatientsForm(request.args)
    if not form.validate():
        return f"Submitted params are invalid: {form.errors}", 422

    # TODO: implement
    return jsonify([])


def patients_post():
    # TODO: implement
    return jsonify({'status': 'OK'})


def _get_payments(payment_min, payment_max):
    query = db.session.query(Payment)
    if payment_min:
        query = query.filter(Payment.amount >= payment_min)
    if payment_max:
        query = query.filter(Payment.amount <= payment_max)

    payments_list = query.all()
    payments_json = getPaymentsSchema.dump(payments_list)

    amount_total = reduce(
        lambda x, y: x + y,
        map(
            lambda x: x.amount,
            payments_list
        ),
        0)

    return payments_json, amount_total


def payments_get():
    form = GetPaymentsForm(request.args)
    if not form.validate():
        return f"Submitted params are invalid: {form.errors}", 422

    payments_list, payments_sum = _get_payments(form.data["payment_min"], form.data["payment_max"])
    return jsonify({"payments": payments_list, "sum": payments_sum})


def payments_post():
    # TODO: implement
    return jsonify({'status': 'OK'})


@api.route('/patients', methods=['POST', 'GET'])
def patients():
    method = patients_post if request.method == 'POST' else patients_get
    return method()


@api.route('/payments', methods=['POST', 'GET'])
def payments():
    method = payments_post if request.method == 'POST' else payments_get
    return method()
