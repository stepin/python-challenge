import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import datetime
from .guid import GUID

db = SQLAlchemy()


class Base(object):
    __abstract__ = True
    id = sa.Column(sa.Integer, primary_key=True)
    created = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    updated = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=datetime.datetime.now, nullable=False)


Base = declarative_base(cls=Base)


class Patient(Base):
    __tablename__ = 'patients'
    __table_args__ = {'sqlite_autoincrement': True}

    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    middle_name = sa.Column(sa.String)
    date_of_birth = sa.Column(sa.Date)
    external_id = sa.Column(sa.String, nullable=False, index=True, unique=True)
    sync_id = sa.Column(GUID)

    def __repr__(self):
        return f"<Patient {self.id} {self.external_id} {self.sync_id} {self.first_name} {self.last_name}>"


class Payment(Base):
    __tablename__ = 'payments'
    __table_args__ = {'sqlite_autoincrement': True}

    amount = sa.Column(sa.Float, nullable=False, index=True)
    patient_id = sa.Column(sa.Integer, sa.ForeignKey('patients.id'), nullable=False)
    patient = db.relationship('Patient', backref=db.backref('payments', lazy=True))
    external_id = sa.Column(sa.String, nullable=False, index=True, unique=True)
    sync_id = sa.Column(GUID)

    def __repr__(self):
        return f"<Payment {self.id} {self.external_id} {self.sync_id} {self.amount} {self.patient_id}>"
