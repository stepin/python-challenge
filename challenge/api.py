from flask import Blueprint, jsonify, request

from challenge.forms import GetPaymentsForm, GetPatientsForm

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
    # TODO: implement
    return [{"min": payment_min, "max": payment_max}], 123


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
