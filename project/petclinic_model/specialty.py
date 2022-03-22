from sqlalchemy import Sequence
from wtforms import SubmitField

from project.app_config.database import db, items_per_page, ModelForm, app


class Specialty(db.Model):
    """
    .. uml:: entities.uml
    .. uml:: specialty.uml
    """
    __tablename__ = "petclinic_specialty"

    all_entity_id_seq = Sequence('id_seq_petclinic_specialty')
    id = db.Column(db.Integer,
                   all_entity_id_seq,
                   server_default=all_entity_id_seq.next_value(),
                   primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name

    @classmethod
    def search(cls, searchterm: str):
        return cls.__query_all().all()

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


class SpecialtyForm(ModelForm):
    """
    .. uml:: entities.uml
    .. uml:: specialty.uml
    """
    class Meta:
        model = Specialty

    submit = SubmitField('Save Specialty')


class SpecialtyService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" SpecialtyService [init]")
