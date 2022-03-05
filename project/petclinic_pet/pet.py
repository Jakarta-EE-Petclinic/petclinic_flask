from sqlalchemy import Sequence

from project.app_config.database import db, items_per_page
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField


class PetForm(FlaskForm):
    name = StringField('Name')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    submit = SubmitField('Save New Pet')


class Pet(db.Model):
    __tablename__ = "petclinic_pet"

    all_entity_id_seq = Sequence('id_seq_petclinic_pet')
    id = db.Column(db.Integer,
                   all_entity_id_seq,
                   server_default=all_entity_id_seq.next_value(),
                   primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

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
