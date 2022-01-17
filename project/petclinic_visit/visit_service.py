from project.app_config.database import app


class VisitService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" VisitService [init]")
