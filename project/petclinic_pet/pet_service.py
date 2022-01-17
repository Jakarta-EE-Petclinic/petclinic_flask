from project.app_config.database import app


class PetService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" PetService [init]")
