from sqlalchemy import Sequence

from project.app_config.database import db, items_per_page
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

from project.petclinic_specialty.specialty import Specialty

specialities_table = db.Table(
    'petclinic_vet_specialities',
    db.Column(
        'vet_id',
        db.Integer,
        db.ForeignKey('petclinic_vet.id'),
        primary_key=True
    ),
    db.Column(
        'specialty_id',
        db.Integer,
        db.ForeignKey('petclinic_specialty.id'),
        primary_key=True
    )
)


class VetForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    submit = SubmitField('Save New Vet')


class Vet(db.Model):
    __tablename__ = "petclinic_vet"

    all_entity_id_seq = Sequence('id_seq_petclinic_vet')
    id = db.Column(
        db.Integer,
        all_entity_id_seq,
        server_default=all_entity_id_seq.next_value(),
        primary_key=True
    )
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    specialities = db.relationship(
        'Specialty', secondary=specialities_table, lazy='subquery',
        backref=db.backref('vets', lazy=True)
    )

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
