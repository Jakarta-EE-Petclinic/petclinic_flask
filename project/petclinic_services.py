from project.petclinic_model import app


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
