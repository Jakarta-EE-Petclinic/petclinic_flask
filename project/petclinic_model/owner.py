from flask_sqlalchemy import Pagination
from sqlalchemy import Sequence
from wtforms import SubmitField

from project.app_config.database import db, items_per_page, ModelForm, app


class Owner(db.Model):
    """
    .. uml:: entities.uml
    .. uml:: owner.uml
    """
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

    def __str__(self):
        return self.first_name + " " + self.last_name + ", " + self.city

    @classmethod
    def prepare_search(cls):
        sql = [
            "ALTER TABLE petclinic_owner ADD COLUMN ts tsvector GENERATED ALWAYS AS (to_tsvector('english', first_name || ' ' || last_name || ' ' || city || ' ' || petclinic_owner.street_address)) STORED;",
            "CREATE INDEX ts_idx ON petclinic_owner USING GIN (ts);"
        ]
        unbuffered = True
        for sql_statement in sql:
            db.session.query(sql_statement, unbuffered)
        db.session.commit()
        return None

    @classmethod
    def search(cls, searchterm: str, page: int):
        sql = "SELECT * FROM petclinic_owner WHERE ts @@ to_tsquery(\'english\', \'"+searchterm+"\')"
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


class OwnerNewForm(ModelForm):
    """
    .. uml:: entities.uml
    .. uml:: owner.uml
    """
    class Meta:
        model = Owner

    cancel = SubmitField('Cancel')
    submit = SubmitField('Save New Owner')


class OwnerShowForm(ModelForm):
    """
    .. uml:: entities.uml
    .. uml:: owner.uml
    """
    class Meta:
        model = Owner

    cancel = SubmitField('Cancel')
    submit = SubmitField('Edit this Owner')


class OwnerEditForm(ModelForm):
    """
    .. uml:: entities.uml
    .. uml:: owner.uml
    """
    class Meta:
        model = Owner

    cancel = SubmitField('Cancel')
    submit = SubmitField('Save this Owner')


class OwnerService:
    def __init__(self, database):
        self.__database = database
        app.logger.info("  OwnerService [init]")
