from project.app_config.database import app
from project.app_user.user import LoginForm
from project.app_user.user import User


class UserService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" UserService [init]")

    def set_database(self, database):
        self.__database = database

    def get_user_from_login_form(self, form: LoginForm):
        user = User()
        user.email = form.email
        user.password = form.password
        return user

    def prepare_default_user_login(self):
        app.logger.info(" UserService.prepare_default_user_login()")
        if User.count() == 0:
            app.logger.debug("-------------------------------------------------------")
            app.logger.info(" User.count() == 0")
            login = app.config["USER_ADMIN_LOGIN"]
            name = app.config["USER_ADMIN_USERNAME"]
            pw = app.config["USER_ADMIN_PASSWORD"]
            user = User.create_new(email=login, name=name, password_hash=pw)
            app.logger.info(user)
            self.__database.session.add(user)
            self.__database.session.commit()
            app.logger.debug("-------------------------------------------------------")
        else:
            app.logger.debug("-------------------------------------------------------")
            app.logger.info(" User.count() > 0")
            app.logger.debug("-------------------------------------------------------")

