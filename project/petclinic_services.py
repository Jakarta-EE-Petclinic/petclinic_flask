from project.petclinic_model import Owner, Pet, PetType, Visit, Vet, Specialty
from project.petclinic_model import db, items_per_page, app


class OwnerService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" OwnerService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info("  OwnerService [done]")
        app.logger.debug("-----------------------------------------------------------")


class PetService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" PetService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" PetService [done]")
        app.logger.debug("-----------------------------------------------------------")


class PetTypeService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" PetTypeService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" PetTypeService [done]")
        app.logger.debug("-----------------------------------------------------------")


class VisitService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" VisitService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" VisitService [done]")
        app.logger.debug("-----------------------------------------------------------")


class VetService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" VetService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" VetService [done]")
        app.logger.debug("-----------------------------------------------------------")


class SpecialtyService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" SpecialtyService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" SpecialtyService [done]")
        app.logger.debug("-----------------------------------------------------------")


class SysAdminService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" SysAdminService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" SysAdminService [done]")
        app.logger.debug("-----------------------------------------------------------")
