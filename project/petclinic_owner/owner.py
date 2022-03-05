from sqlalchemy import Sequence

from project.app_config.database import db, items_per_page
from flask_wtf import FlaskForm
from wtforms import StringField, TelField, EmailField, SubmitField


class OwnerForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    street_address = StringField('Address')
    zip_code = StringField('ZIP Code')
    city = StringField('City')
    telephone = TelField('Telephone')
    email = EmailField('Email')
    submit = SubmitField('Save New Owner')


class Owner(db.Model):
    __tablename__ = "petclinic_owner"

    all_entity_id_seq = Sequence('id_seq_petclinic_owner')
    id = db.Column(db.Integer,
                   all_entity_id_seq,
                   server_default=all_entity_id_seq.next_value(),
                   primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    street_address = db.Column(db.String(1024), nullable=False)
    zip_code = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    @classmethod
    def remove_all(cls):
        db.session.query(cls).delete()
        db.session.commit()
        return None

    @classmethod
    def __query_all(cls):
        return db.session.query(cls)

    @classmethod
    def get_all(cls, page: int):
        return cls.__query_all().paginate(page, per_page=items_per_page)

    @classmethod
    def find_all(cls):
        return cls.__query_all().all()

    @classmethod
    def find_all_as_dict(cls):
        pass

    @classmethod
    def find_all_as_str(cls):
        pass

    @classmethod
    def get_by_id(cls, other_id):
        return cls.__query_all().filter(cls.id == other_id).one()

    @classmethod
    def find_by_id(cls, other_id):
        return cls.__query_all().filter(cls.id == other_id).one_or_none()
