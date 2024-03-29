from flask_sqlalchemy import Pagination
from sqlalchemy import Sequence
from wtforms import SubmitField
from wtforms.validators import InputRequired
from wtforms_alchemy import QuerySelectField

from project.app_config.database import db, items_per_page, ModelForm, app
from project.petclinic_model.pet import Pet


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

    @classmethod
    def prepare_search(cls):
        sql = [
            "ALTER TABLE petclinic_visit ADD COLUMN ts tsvector GENERATED ALWAYS AS (to_tsvector('english', information)) STORED;",
            "CREATE INDEX ts_idx ON petclinic_visit USING GIN (ts);"
        ]
        unbuffered = True
        for sql_statement in sql:
            db.session.query(sql_statement, unbuffered)
        db.session.commit()
        return None

    @classmethod
    def search(cls, searchterm: str, page: int):
        unbuffered = True
        sql = "SELECT * "\
            + "FROM petclinic_visit " \
            + "WHERE ts @@ to_tsquery('english', '"+searchterm+"');"
        query = db.session.execute(sql)
        list = query.fetchall()
        result_page = Pagination(
            query=query, page=page,
            per_page=items_per_page, total=len(list),
            items=list
        )
        return result_page

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
    submit = SubmitField('Save Visit')


class VisitService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" VisitService [init]")
