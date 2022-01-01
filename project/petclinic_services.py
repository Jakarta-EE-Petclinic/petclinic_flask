from project.petclinic_model import Owner, Pet, PetType, Visit, Vet, Specialty
from project.petclinic_model import items_per_page, db, app


class OwnerService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" OwnerService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info("  OwnerService [ready]")
        app.logger.debug("-----------------------------------------------------------")


class PetService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" PetService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" PetService [ready]")
        app.logger.debug("-----------------------------------------------------------")


class PetTypeService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" PetTypeService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" PetTypeService [ready]")
        app.logger.debug("-----------------------------------------------------------")


class VisitService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" VisitService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" VisitService [ready]")
        app.logger.debug("-----------------------------------------------------------")


class VetService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" VetService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" VetService [ready]")
        app.logger.debug("-----------------------------------------------------------")


class SpecialtyService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" SpecialtyService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" SpecialtyService [ready]")
        app.logger.debug("-----------------------------------------------------------")


class SysAdminService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" SysAdminService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" SysAdminService [ready]")
        app.logger.debug("-----------------------------------------------------------")

    def database_dump(self):
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" database_dump [start]")
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" ")
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" database_dump [done]")
        app.logger.info("-----------------------------------------------------------")

    def database_dump_reimport(self):
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" database_dump_reimport [start]")
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" ")
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" database_dump_reimport [done]")
        app.logger.info("-----------------------------------------------------------")

    def database_drop_and_create(self):
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" database_drop_and_create [start]")
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" ")
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" database_drop_and_create [done]")
        app.logger.info("-----------------------------------------------------------")

    def database_table_row_count(self):
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" database_table_row_count [start]")
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" ")
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" database_table_row_count [done]")
        app.logger.info("-----------------------------------------------------------")
