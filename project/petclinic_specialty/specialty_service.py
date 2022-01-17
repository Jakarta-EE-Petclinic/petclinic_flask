from project.app_config.database import app


class SpecialtyService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" SpecialtyService [init]")
