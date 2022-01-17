import flask
from flask import Blueprint, flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.exc import OperationalError

from project.app_config.database import db, login_manager
from project.app_user.user import LoginForm, User
from project.app_user.user_service import UserService
from project.app_web.web_model_transient import WebPageContent
from project.app_web.admin_services import db, app
from project.app_web.admin_services import SysAdminService
from project.petclinic_owner.owner_service import OwnerService
from project.petclinic_pet.pet_service import PetService
from project.petclinic_pettype.pettype_service import PetTypeService
from project.petclinic_specialty.specialty_service import SpecialtyService
from project.petclinic_vet.vet_service import VetService
from project.petclinic_visit.visit_service import VisitService
from project.app_notification.notification import Notification
from project.app_notification.notification_service import NotificationService

task_service = NotificationService(db)
owner_service = OwnerService(db)
pet_service = PetService(db)
pet_type_service = PetTypeService(db)
visit_service = VisitService(db)
vet_service = VetService(db)
specialty_service = SpecialtyService(db)
sys_admin_service = SysAdminService(db)
user_service = UserService(db)

app_user = Blueprint(
    "app_user", __name__, template_folder="templates", url_prefix="/app_user"
)

app_web = Blueprint(
    "app_web", __name__, template_folder="templates", url_prefix="/"
)

app.register_blueprint(app_web, url_prefix="/")
app.register_blueprint(app_user, url_prefix="/app_user")


class ApplicationUrls:
    def __init__(self):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [WEB] ApplicationUrls ")
        app.logger.debug("-----------------------------------------------------------")

    @staticmethod
    @app.route("/home")
    def url_home():
        page_info = WebPageContent("Home", "Petclinic")
        return render_template(
            "app_application/page_home.html",
            page_info=page_info
        )

    @staticmethod
    @app.route("/")
    def url_root():
        return redirect(url_for("url_home"))

    @staticmethod
    @app.route("/admin")
    def url_admin_index():
        page_info = WebPageContent("Admin", "Petclinic")
        return render_template(
            "app_application/index.html",
            page_info=page_info
        )

    @staticmethod
    @app.route("/owner")
    def url_owner_index():
        page_info = WebPageContent("petclinic_owner", "index")
        return render_template(
            "petclinic_owner/index.html",
            page_info=page_info
        )

    @staticmethod
    @app.route("/pet")
    def url_pet_index():
        page_info = WebPageContent("petclinic_pet", "index")
        return render_template(
            "petclinic_pet/index.html",
            page_info=page_info
        )

    @staticmethod
    @app.route("/pettype")
    def url_pettype_index():
        page_info = WebPageContent("petclinic_pettype", "index")
        return render_template(
            "petclinic_pettype/index.html",
            page_info=page_info
        )

    @staticmethod
    @app.route("/visit")
    def url_visit_index():
        page_info = WebPageContent("petclinic_visit", "index")
        return render_template(
            "petclinic_visit/index.html",
            page_info=page_info
        )

    @staticmethod
    @app.route("/vet")
    def url_vet_index():
        page_info = WebPageContent("petclinic_vet", "index")
        return render_template(
            "petclinic_vet/index.html",
            page_info=page_info
        )

    @staticmethod
    @app.route("/specialty")
    def url_specialty_index():
        page_info = WebPageContent("petclinic_specialty", "index")
        return render_template(
            "petclinic_specialty/index.html",
            page_info=page_info
        )

    @staticmethod
    @app.route("/notification/page/<int:page>")
    @app.route("/notification")
    @login_required
    def url_all_notification(page=1):
        page_info = WebPageContent("All", "Notifications")
        page_data = Notification.notifications_get(page)
        return render_template("app_all/notification/app_all_notification.html",
                               page_data=page_data,
                               page_info=page_info)

    @staticmethod
    @app.route("/notification/read/page/<int:page>")
    @app.route("/notification/read")
    @login_required
    def url_all_notification_mark_read(page=1):
        page_data = Notification.notifications_get(page)
        for o in page_data.items:
            o.read()
            db.session.add(o)
        db.session.commit()
        return redirect(url_for("url_all_notification"))

    @staticmethod
    @app.route("/login", methods=["GET"])
    def login_form():
        page_info = WebPageContent("app_user", "Login")
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        form = LoginForm()
        return flask.render_template(
            "app_user/login.html",
            form=form,
            page_info=page_info
        )

    @staticmethod
    @app.route("/login", methods=["POST"])
    def login():
        page_info = WebPageContent("USR", "Login")
        if current_user.is_authenticated:
            return redirect(url_for("profile"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password")
                return redirect(url_for("login"))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("profile"))
        return flask.render_template("app_user/login.html", form=form, page_info=page_info)

    @staticmethod
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @staticmethod
    @app.route("/profile")
    @login_required
    def profile():
        page_info = WebPageContent("USR", "profile")
        return flask.render_template("app_user/profile.html", page_info=page_info)

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    @staticmethod
    @login_manager.unauthorized_handler
    def unauthorized():
        flash("not authorized")
        return redirect(url_for("login"))

    @staticmethod
    @app.route("/info/page/<int:page>")
    @app.route("/info")
    def url_user_info(page=1):
        page_info = WebPageContent("USR", "Info")
        try:
            page_data = User.get_all_as_page(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "app_user/user_info.html", page_data=page_data, page_info=page_info
        )

    @staticmethod
    @app_user.route("/tasks")
    def url_user_tasks():
        page_info = WebPageContent("USR", "Tasks")
        return render_template("app_user/user_tasks.html", page_info=page_info)


app_web_urls = ApplicationUrls()

# ------------------------------------------------------------------------------------
# URLs Login and Logout
# ------------------------------------------------------------------------------------


class AppUserUrls:
    def __init__(self):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [USR] UserUrls ")
        app.logger.debug("-----------------------------------------------------------")

    # ---------------------------------------------------------------------------------
    #  Url Routes Frontend
    # ---------------------------------------------------------------------------------


app_user_urls = AppUserUrls()
