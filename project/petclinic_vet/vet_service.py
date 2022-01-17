from project.app_config.database import app


class VetService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" VetService [init]")
