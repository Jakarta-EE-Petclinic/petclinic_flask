
import click

from project.petclinic_views import Owner, Pet, PetType, Visit, Vet, Specialty
from project.petclinic_views import items_per_page, db, app
from project.petclinic_views import owner_service, pet_service, pet_type_service
from project.petclinic_views import visit_service, vet_service, specialty_service
from project.petclinic_views import sys_admin_service, app_web


def create_app():
    # run_web()
    with app.app_context():
        db.create_all()
    return app


@app.cli.command("db-create")
def admin_database_dump():
    """[Admin] database create"""
    with app.app_context():
        db.create_all()


@app.cli.command("db-dump")
def admin_database_dump():
    """[Admin] database dump"""
    with app.app_context():
        sys_admin_service.database_dump()


@app.cli.command("db-dump-reimport")
def admin_database_dump_reimport():
    """[Admin] database dump reimport"""
    with app.app_context():
        sys_admin_service.database_dump_reimport()


@app.cli.command("db-drop-and-create")
def admin_database_drop_and_create():
    """[Admin] database drop and create"""
    with app.app_context():
        sys_admin_service.database_drop_and_create()


@app.cli.command("db-table-count")
def admin_database_table_row_count():
    """[Admin] database table row count"""
    with app.app_context():
        sys_admin_service.database_table_row_count()


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
