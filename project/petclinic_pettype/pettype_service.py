from project.app_config.database import app


class PetTypeService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" PetTypeService [init]")
