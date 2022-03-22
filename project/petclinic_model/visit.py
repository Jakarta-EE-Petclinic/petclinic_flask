from sqlalchemy import Sequence
from wtforms import SubmitField
from wtforms.validators import InputRequired
from wtforms_alchemy import QuerySelectField

from project.app_config.database import db, items_per_page, ModelForm, app
from project.petclinic_model.pet import Pet
from project.petclinic_model.vet import Vet


class Visit(db.Model):
    """
    .. uml:: entities.uml
    .. uml:: visit.uml
    """
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
    vet_id = db.Column(
        db.Integer, db.ForeignKey("petclinic_vet.id"), nullable=False
    )
    vet = db.relationship(
        "Vet",
        lazy="joined",
        cascade="save-update",
        order_by="asc(Vet.last_name)",
        backref=db.backref('visits', lazy=True)
    )

    @classmethod
    def search(cls, searchterm: str):
        return cls.__query_all().all()

    @classmethod
    def find_by_pet(cls, pet: Pet):
        return db.session.query(cls).filter(cls.pet_id == pet.id).all()

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
    """
    .. uml:: entities.uml
    .. uml:: visit.uml
    """
    class Meta:
        model = Visit

    pet_select = QuerySelectField(
        'pet_select', [InputRequired('Bitte waehlen Sie ein Pet aus')],
        Pet.find_all,
        lambda p: p.id, lambda p: p.__str__(),
        True, 'Bitte waehlen Sie ein Pet aus',
    )
    vet_select = QuerySelectField(
        'vet_select', [InputRequired('Bitte waehlen Sie ein Vet aus')],
        Vet.find_all,
        lambda v: v.id, lambda v: v.__str__(),
        True, 'Bitte waehlen Sie ein Vet aus',
    )
    submit = SubmitField('Save Visit')


class VisitService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" VisitService [init]")
