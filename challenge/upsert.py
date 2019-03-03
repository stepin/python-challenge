from challenge import db

patient_upsert_sql = """
INSERT INTO patients(external_id,first_name,last_name,date_of_birth,sync_id)
  VALUES(?)
  ON CONFLICT(external_id) DO UPDATE SET
    first_name=excluded.first_name,
    last_name=excluded.last_name,
    date_of_birth=excluded.date_of_birth,
    updated=CURRENT_TIMESTAMP,
    sync_id=excluded.sync_id;
"""
payment_upsert_sql = """
INSERT INTO payments(external_id,patient_id,amount,sync_id)
  VALUES(?)
  ON CONFLICT(external_id) DO UPDATE SET
    patient_id=excluded.patient_id,
    amount=excluded.amount,
    updated=CURRENT_TIMESTAMP,
    sync_id=excluded.sync_id;
"""


def _upsert(model, values):
    sql = f"SELECT * FROM {model}"
    db.engine.execute(sql)


def split_to_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


# NOTE: no support for bulk upsert in the sqlalchemy
def upsert(model, values):
    chunks = split_to_chunks(values, 1000)
    for chunk in chunks:
        _upsert(model, chunk)
