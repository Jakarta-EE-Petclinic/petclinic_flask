
import click

from project.petclinic_views import Owner, Pet, PetType, Visit, Vet, Specialty
from project.petclinic_views import db, items_per_page, app
from project.petclinic_views import owner_service, pet_service, pet_type_service
from project.petclinic_views import visit_service, vet_service, specialty_service
from project.petclinic_views import sys_admin_service


def create_app():
    # run_web()
    with app.app_context():
        db.create_all()
    return app


@app.cli.command("admin-database-dump")
def admin_database_dump():
    """[Admin] database dump"""
    with app.app_context():
        sys_admin_service.database_dump()


@app.cli.command("admin-database-dump-reimport")
def admin_database_dump_reimport():
    """[Admin] database dump reimport"""
    with app.app_context():
        sys_admin_service.database_dump_reimport()


@app.cli.command("admin-database-drop-and-create")
def admin_database_drop_and_create():
    """[Admin] database drop and create"""
    with app.app_context():
        sys_admin_service.database_drop_and_create()


@app.cli.command("admin-database-table-row-count")
def admin_database_table_row_count():
    """[Admin] database table row count"""
    with app.app_context():
        sys_admin_service.database_table_row_count()


# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    db.create_all()
    # run_web()
