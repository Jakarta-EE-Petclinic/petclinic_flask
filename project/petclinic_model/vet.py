from flask_sqlalchemy import Pagination
from sqlalchemy import Sequence
from wtforms import SubmitField
from wtforms.validators import InputRequired
from wtforms_alchemy import QuerySelectField, QuerySelectMultipleField

from project.app_config.database import db, items_per_page, ModelForm, app
from project.petclinic_model.specialty import Specialty

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
visits_table = db.Table(
    'petclinic_vet_visits',
    db.Column(
        'vet_id',
        db.Integer,
        db.ForeignKey('petclinic_vet.id'),
        primary_key=True
    ),
    db.Column(
        'specialty_id',
        db.Integer,
        db.ForeignKey('petclinic_visit.id'),
        primary_key=True
    )
)


class Vet(db.Model):
    """
    .. uml:: entities.uml
    .. uml:: vet.uml
    """
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
    #visits = db.relationship(
    #    'Visit', secondary=visits_table, lazy='subquery',
    #    backref=db.backref('visits', lazy=True)
    #)

    def __str__(self):
        return self.first_name + " " + self.last_name

    @classmethod
    def prepare_search(cls):
        sql = [
            "ALTER TABLE petclinic_vet ADD COLUMN ts tsvector GENERATED ALWAYS AS (to_tsvector('english', first_name || ' ' || last_name)) STORED;",
            "CREATE INDEX ts_idx ON petclinic_vet USING GIN (ts);"
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
            + "FROM petclinic_vet " \
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


class VetForm(ModelForm):
    class Meta:
        model = Vet

    specialty_select = QuerySelectMultipleField(
        label='specialty_select',
        validators=[InputRequired('Bitte waehlen Sie ein Specialty aus')],
        default=[],
        query_factory=Specialty.find_all,
        get_pk=lambda x: x.id, get_label=lambda x: x.__str__()
    )
    submit = SubmitField('Save Vet')


class VetService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" VetService [init]")
