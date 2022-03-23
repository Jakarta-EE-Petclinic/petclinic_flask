from project.petclinic_model.specialty import Specialty
from project.petclinic_model.vet import Vet
from project.petclinic_model.pettype import PetType
from project.petclinic_model.visit import Visit
from project.petclinic_model.pet import Pet
from project.petclinic_model.owner import Owner

from project.petclinic_views import db, app
from project.petclinic_views import admin_service, user_service


def create_app():
    # run_web()
    with app.app_context():
        db.create_all()
        Owner.prepare_search()
        Pet.prepare_search()
        Visit.prepare_search()
        PetType.prepare_search()
        Vet.prepare_search()
        Specialty.prepare_search()
    user_service.prepare_default_user_login()
    return app


@app.cli.command("db-create")
def admin_database_dump():
    """[Admin] database create"""
    with app.app_context():
        db.create_all()
        user_service.prepare_default_user_login()


@app.cli.command("db-dump")
def admin_database_dump():
    """[Admin] database dump"""
    with app.app_context():
        admin_service.database_dump()


@app.cli.command("db-dump-reimport")
def admin_database_dump_reimport():
    """[Admin] database dump reimport"""
    with app.app_context():
        admin_service.database_dump_reimport()


@app.cli.command("db-drop-and-create")
def admin_database_drop_and_create():
    """[Admin] database drop and create"""
    with app.app_context():
        admin_service.database_drop_and_create()


@app.cli.command("db-table-count")
def admin_database_table_row_count():
    """[Admin] database table row count"""
    with app.app_context():
        admin_service.database_table_row_count()


# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    app.logger.info("----------------------------------------------------")
    app.logger.info("                     MAIN                           ")
    create_app()
    with app.app_context():
        db.create_all()
    app.logger.info("----------------------------------------------------")
    # run_web()
