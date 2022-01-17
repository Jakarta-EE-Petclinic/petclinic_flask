import os
import sys
from logging.config import dictConfig

from flask import Flask
from flask_admin import Admin
from flask_bs4 import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from project.app_config import config
from project.app_config import pytestconfig


class PetclinicApplication:
    def __init__(self, testing=False):
        self.app = Flask("flask_petclinic")
        self.app_cors = CORS()
        if testing:
            self.app.config.from_object(pytestconfig)
        else:
            self.app.config.from_object(config)
        self.__init_db()
        self.__init_login()
        self.__init_bootstrap()
        self.__init_admin()
        self.__init_loging()
        oo_list = [
            self.db,
            self.app_cors,
            self.login_manager,
            self.app_bootstrap
        ]
        for oo in oo_list:
            oo.init_app(self.app)
        self.root_dir = os.getcwd()
        self.__print_config()

    def __init_db(self):
        self.db = SQLAlchemy()
        self.database_type = self.app.config["SQLALCHEMY_DATABASE_TYPE"]
        self.db_uri = self.__create_db_uri(self.database_type)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
        self.app.config[ "SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.items_per_page = self.app.config["SQLALCHEMY_ITEMS_PER_PAGE"]
        return self

    def __init_bootstrap(self):
        self.app_bootstrap = Bootstrap()
        self.app.config["BOOTSTRAP_SERVE_LOCAL"] = True
        self.app.config["BOOTSTRAP_USE_CDN"] = False
        self.app.config["BOOTSTRAP_CUSTOM_CSS"] = True
        return self

    def __init_login(self):
        self.login_manager = LoginManager()
        self.login_manager.login_view = "login"
        return self

    def __init_admin(self):
        self.app.config["FLASK_ADMIN_SWATCH"] = "darkly"
        self.admin = Admin(
            self.app,
            name="Petclinic | admin",
            template_mode="bootstrap5"
        )
        return self

    def __init_loging(self):
        self.logging_config = {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
        dictConfig(self.logging_config)
        return self

    def __create_db_uri(self, database_type: str):
        if database_type == "mariadb":
            return "mariadb+mariadbconnector://{user}:{pw}@{url}/{db}".format(
                user=self.app.config["SQLALCHEMY_DATABASE_USER"],
                pw=self.app.config["SQLALCHEMY_DATABASE_PW"],
                url=self.app.config["SQLALCHEMY_DATABASE_HOST"],
                db=self.app.config["SQLALCHEMY_DATABASE_DB"],
            )
        if database_type == "postgresql":
            return "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
                user=self.app.config["SQLALCHEMY_DATABASE_USER"],
                pw=self.app.config["SQLALCHEMY_DATABASE_PW"],
                url=self.app.config["SQLALCHEMY_DATABASE_HOST"],
                db=self.app.config["SQLALCHEMY_DATABASE_DB"],
            )
        if database_type == "mysql":
            return "mysql://{user}:{pw}@{url}/{db}".format(
                user=self.app.config["SQLALCHEMY_DATABASE_USER"],
                pw=self.app.config["SQLALCHEMY_DATABASE_PW"],
                url=self.app.config["SQLALCHEMY_DATABASE_HOST"],
                db=self.app.config["SQLALCHEMY_DATABASE_DB"],
            )
        return None

    def get_db(self):
        self.__init_db()
        with app.app_context():
            db.create_all()
        return self.db

    def create_db(self):
        with app.app_context():
            db.create_all()
        return self

    def __print_config(self):
        self.app.logger.debug("------------------------------------------------------")
        for key in self.app.config.keys():
            self.app.logger.debug(" " + str(key) + " " + str(self.app.config[key]))
        self.app.logger.debug("------------------------------------------------------")


petclinic_application = PetclinicApplication()
app = petclinic_application.app
db = petclinic_application.db
admin = petclinic_application.admin
root_dir = petclinic_application.root_dir
login_manager = petclinic_application.login_manager
items_per_page = petclinic_application.items_per_page

petclinic_application.create_db()
