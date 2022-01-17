from project.app_config.database import app


class OwnerService:
    def __init__(self, database):
        self.__database = database
        app.logger.info("  OwnerService [init]")
