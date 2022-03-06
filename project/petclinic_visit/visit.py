from sqlalchemy import Sequence

from project.app_config.database import db, items_per_page, ModelForm
from flask_wtf import FlaskForm
from wtforms import DateField, TextAreaField, SubmitField
from wtforms.validators import InputRequired

from project.petclinic_pet.pet import Pet


class Visit(db.Model):
    __tablename__ = "petclinic_visit"

    all_entity_id_seq = Sequence('all_entity_id_seq')
    id = db.Column(db.Integer,
                   all_entity_id_seq,
                   server_default=all_entity_id_seq.next_value(),
                   primary_key=True)
    datum = db.Column(db.Date, nullable=False)
    information = db.Column(db.String(1024), nullable=False)
    pet_id = db.Column(
        db.Integer, db.ForeignKey("petclinic_pet.id"), nullable=False
    )
    pet = db.relationship(
        "Pet",
        lazy="joined",
        cascade="save-update",
        order_by="asc(Pet.date_of_birth)",
        backref=db.backref('visits', lazy=True)
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


class VisitForm(ModelForm):
    class Meta:
        model = Visit

    datum = DateField('Date of Visit', format='%Y-%m-%d', validators=[InputRequired()])
    information = TextAreaField('information', validators=[InputRequired()])
    submit = SubmitField('Save New Visit')
