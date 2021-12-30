import flask
from flask import Blueprint, flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.exc import OperationalError

from project.config.database import login_manager
from project.model.user_model import LoginForm, User
from project.model.web_model_transient import WebPageContent
from project.petclinic_services import Owner, Pet, PetType, Visit, Vet, Specialty
from project.petclinic_services import db, items_per_page, app, celery
from project.petclinic_services import OwnerService, PetService, PetTypeService
from project.petclinic_services import VisitService, VetService, SpecialtyService


blueprint_app_user = Blueprint(
    "usr", __name__, template_folder="templates", url_prefix="/app/usr"
)

class BlueprintApplicationUrls:
    def __init__(self):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [WEB] ApplicationUrls ")
        app.logger.debug("-----------------------------------------------------------")

    @staticmethod
    @app.route("/home")
    def url_home():
        page_info = WebPageContent("Home", "Covid19 Data")
        return render_template("app_application/page_home.html", page_info=page_info)

    @staticmethod
    @app.route("/")
    def url_root():
        return redirect(url_for("url_home"))

    @staticmethod
    @app.route("/admin")
    def url_admin_index():
        page_info = WebPageContent("Admin", "Covid19 Admin")
        return render_template("app_application/index.html", page_info=page_info)


blueprint_application_urls = BlueprintApplicationUrls()



blueprint_app_user = Blueprint(
    "usr", __name__, template_folder="templates", url_prefix="/app/usr"
)


# ------------------------------------------------------------------------------------
# URLs Login and Logout
# ------------------------------------------------------------------------------------


class AppUserUrls:
    def __init__(self):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [USR] UserUrls ")
        app.logger.debug("-----------------------------------------------------------")

    @staticmethod
    @blueprint_app_user.route("/login", methods=["GET"])
    def login_form():
        page_info = WebPageContent("usr", "Login")
        if current_user.is_authenticated:
            return redirect(url_for("usr.profile"))
        form = LoginForm()
        return flask.render_template("usr/login.html", form=form, page_info=page_info)

    @staticmethod
    @blueprint_app_user.route("/login", methods=["POST"])
    def login():
        page_info = WebPageContent("USR", "Login")
        if current_user.is_authenticated:
            return redirect(url_for("usr.profile"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password")
                return redirect(url_for("usr.login"))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("usr.profile"))
        return flask.render_template("usr/login.html", form=form, page_info=page_info)

    @staticmethod
    @blueprint_app_user.route("/profile")
    @login_required
    def profile():
        page_info = WebPageContent("USR", "profile")
        return flask.render_template("usr/profile.html", page_info=page_info)

    @staticmethod
    @blueprint_app_user.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("usr.login"))

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    @staticmethod
    @login_manager.unauthorized_handler
    def unauthorized():
        flash("not authorized")
        return redirect(url_for("usr.login"))

    # ---------------------------------------------------------------------------------
    #  Url Routes Frontend
    # ---------------------------------------------------------------------------------

    @staticmethod
    @blueprint_app_user.route("/info/page/<int:page>")
    @blueprint_app_user.route("/info")
    def url_user_info(page=1):
        page_info = WebPageContent("USR", "Info")
        try:
            page_data = User.get_all_as_page(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "usr/user_info.html", page_data=page_data, page_info=page_info
        )

    @staticmethod
    @blueprint_app_user.route("/tasks")
    def url_user_tasks():
        page_info = WebPageContent("USR", "Tasks")
        return render_template("usr/user_tasks.html", page_info=page_info)


app_user_urls = AppUserUrls()

