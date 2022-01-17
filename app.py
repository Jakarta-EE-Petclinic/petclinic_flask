
import click

from project.petclinic_owner.owner import Owner
from project.petclinic_pet.pet import Pet
from project.petclinic_pettype.pettype import PetType
from project.petclinic_specialty.specialty import Specialty
from project.petclinic_vet.vet import Vet
from project.petclinic_visit.visit import Visit

from project.petclinic_views import items_per_page, db, app
from project.petclinic_views import owner_service, pet_service, pettype_service
from project.petclinic_views import visit_service, vet_service, specialty_service
from project.petclinic_views import admin_service, app_web, user_service


def create_app():
    # run_web()
    with app.app_context():
        db.create_all()
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
