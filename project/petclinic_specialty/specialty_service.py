class SpecialtyService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" SpecialtyService [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" SpecialtyService [ready]")
        app.logger.debug("-----------------------------------------------------------")
