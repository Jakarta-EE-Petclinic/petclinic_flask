from sqlalchemy import Sequence
from wtforms import SubmitField
from wtforms.validators import InputRequired
from wtforms_alchemy import ModelFormField, QuerySelectField

from project.app_config.database import db, items_per_page, ModelForm, app
from project.petclinic_model.pettype import PetType, PetTypeForm
from project.petclinic_model.owner import Owner, OwnerNewForm


class Pet(db.Model):
    """
    .. uml:: entities.uml
    .. uml:: pet.uml
    """
    __tablename__ = "petclinic_pet"

    all_entity_id_seq = Sequence('id_seq_petclinic_pet')
    id = db.Column(db.Integer,
                   all_entity_id_seq,
                   server_default=all_entity_id_seq.next_value(),
                   primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    owner_id = db.Column(
        db.Integer, db.ForeignKey("petclinic_owner.id"), nullable=False
    )
    owner = db.relationship(
        "Owner",
        lazy="joined",
        cascade="save-update",
        order_by="asc(Owner.last_name)"
    )
    pettype_id = db.Column(
        db.Integer, db.ForeignKey("petclinic_pettype.id"), nullable=False
    )
    pettype = db.relationship(
        "PetType",
        lazy="joined",
        cascade="save-update",
        order_by="asc(PetType.name)"
    )

    def __str__(self):
        return self.name + " - " + \
               self.date_of_birth.isoformat() + " - " + \
               self.pettype.__str__() + ", " + \
               self.owner.__str__()

    @classmethod
    def search(cls, searchterm: str, page: int):
        return cls.__query_all().paginate(page, per_page=items_per_page)

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
    def find_by_owner(cls, owner: Owner):
        return db.session.query(cls).filter(cls.owner_id == owner.id)

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


class PetForm(ModelForm):
    """
    .. uml:: entities.uml
    .. uml:: pet.uml
    """
    class Meta:
        model = Pet

    # owner = ModelFormField(OwnerNewForm)
    # pettype = ModelFormField(PetTypeForm)
    pettype_select = QuerySelectField(
        'pettype_select', [InputRequired('Bitte waehlen Sie einen PetType aus')],
        PetType.find_all,
        lambda x: x.id, lambda x: x.name,
        True, 'Bitte waehlen Sie einen PetType aus',
    )
    owner_select = QuerySelectField(
        'owner_select', [InputRequired('Bitte waehlen Sie einen Owner aus')],
        Owner.find_all,
        lambda x: x.id, lambda x: x.__str__(),
        True, 'Bitte waehlen Sie einen Owner aus',
    )
    submit = SubmitField('Save Pet')


class PetService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" PetService [init]")
