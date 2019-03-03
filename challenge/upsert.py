from .models import db

patient_upsert_sql = """
INSERT INTO patients(external_id,first_name,last_name,date_of_birth,sync_id)
  VALUES(:external_id,:first_name,:last_name,:date_of_birth,:sync_id)
  ON CONFLICT(external_id) DO UPDATE SET
    first_name=excluded.first_name,
    last_name=excluded.last_name,
    date_of_birth=excluded.date_of_birth,
    updated=CURRENT_TIMESTAMP,
    sync_id=excluded.sync_id;
"""
payment_upsert_sql = """
INSERT INTO payments(external_id,patient_id,amount,sync_id)
  VALUES(:external_id,:patient_id,:amount,:sync_id)
  ON CONFLICT(external_id) DO UPDATE SET
    patient_id=excluded.patient_id,
    amount=excluded.amount,
    updated=CURRENT_TIMESTAMP,
    sync_id=excluded.sync_id;
"""


def _upsert(sql, values):
    db.engine.execute(sql, values)


def split_to_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def _add_sync_id(dict, sync_id):
    dict["sync_id"] = sync_id
    return dict


# NOTE: no support for bulk upsert in the sqlalchemy
def upsert(sql, values, sync_id):
    chunks = split_to_chunks(values, 1000)
    for chunk in chunks:
        chunk = list(map(lambda x: _add_sync_id(x, sync_id), chunk))
        _upsert(sql, chunk)


def upsert_patients(patients, sync_id):
    upsert(patient_upsert_sql, patients, sync_id)


def upsert_payments(payments, sync_id):
    upsert(payment_upsert_sql, payments, sync_id)
