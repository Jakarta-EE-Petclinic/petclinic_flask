import flask
from flask import Blueprint, request, flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.exc import OperationalError

from project.app_config.database import app, db, login_manager

from project.app_user.user import LoginForm, User
from project.app_user.user_service import UserService
from project.app_web.web_model_transient import WebPageContent
from project.app_web.admin_services import AdminService
from project.app_notification.notification import Notification
from project.app_notification.notification_service import NotificationService

from project.petclinic_model.owner import Owner, OwnerForm, OwnerService
from project.petclinic_model.pet import Pet, PetForm, PetService
from project.petclinic_model.pettype import PetType, PetTypeForm, PetTypeService
from project.petclinic_model.specialty import Specialty, SpecialtyForm, \
    SpecialtyService
from project.petclinic_model.vet import Vet, VetForm, VetService
from project.petclinic_model.visit import Visit, VisitForm, VisitService

owner_service = OwnerService(db)
pet_service = PetService(db)
pettype_service = PetTypeService(db)
visit_service = VisitService(db)
vet_service = VetService(db)
specialty_service = SpecialtyService(db)

notification_service = NotificationService(db)
admin_service = AdminService(db)
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
        app.logger.info(" ApplicationUrls [init]")
        with app.app_context():
            db.create_all()
            task = Notification.create(sector="WEB", task_name="init")
            user_service.prepare_default_user_login()
            Notification.finish(task_id=task.id)

    @staticmethod
    @app.route("/home")
    def url_home():
        page_info = WebPageContent("Home", "Petclinic")
        return render_template(
            "app_web/page_home.html",
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
            "app_web/index.html",
            page_info=page_info
        )

    @staticmethod
    @app.route("/notification")
    @login_required
    def url_all_notification(page=1):
        page_info = WebPageContent("All", "Notifications")
        page_data = Notification.notifications_get(page)
        return render_template(
            "app_notification/notification/app_all_notification.html",
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


class DomainModelUrls:
    def __init__(self):
        app.logger.info(" DomainModelUrls [init]")

    @staticmethod
    @app.route("/owner")
    def url_owner_index(page=1):
        page_info = WebPageContent("petclinic_owner", "index")
        page_data = Owner.get_all(page)
        return render_template(
            "petclinic_model/owner/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/owner/new", methods=['GET', 'POST'])
    def url_owner_new():
        form = OwnerForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = Owner()
            o.first_name = form.first_name.data
            o.last_name = form.last_name.data
            o.street_address = form.street_address.data
            o.zip_code = form.zip_code.data
            o.city = form.city.data
            o.telephone = form.telephone.data
            o.email = form.email.data
            db.session.add(o)
            db.session.commit()
            return redirect(url_for('url_owner_index'))
        page_info = WebPageContent("petclinic_owner", "new")
        return render_template(
            "petclinic_model/owner/new.html",
            form=form,
            page_info=page_info
        )

    @staticmethod
    @app.route("/pet")
    def url_pet_index(page=1):
        page_info = WebPageContent("petclinic_pet", "index")
        page_data = Pet.get_all(page)
        return render_template(
            "petclinic_model/pet/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/pet/new", methods=['GET', 'POST'])
    def url_pet_new():
        form = PetForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = Pet()
            o.name = form.meta.name.data
            o.date_of_birth = form.meta.date_of_birth.data
            o.owner = form.owner_select.data
            o.pettype = form.pettype_select.data
            db.session.add(o)
            db.session.commit()
            return redirect(url_for('url_pet_index'))
        page_info = WebPageContent("petclinic_pet", "new")
        return render_template(
            "petclinic_model/pet/new.html",
            form=form,
            page_info=page_info
        )

    @staticmethod
    @app.route("/pettype")
    def url_pettype_index(page=1):
        page_info = WebPageContent("petclinic_pettype", "index")
        page_data = PetType.get_all(page)
        return render_template(
            "petclinic_model/pettype/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/pettype/new", methods=['GET', 'POST'])
    def url_pettype_new():
        form = PetTypeForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = PetType()
            o.name = form.name.data
            db.session.add(o)
            db.session.commit()
            return redirect(url_for('url_pettype_index'))
        page_info = WebPageContent("petclinic_pettype", "new")
        return render_template(
            "petclinic_model/pettype/new.html",
            form=form,
            page_info=page_info
        )

    @staticmethod
    @app.route("/visit")
    def url_visit_index(page=1):
        page_info = WebPageContent("petclinic_visit", "index")
        page_data = Visit.get_all(page)
        return render_template(
            "petclinic_model/visit/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/visit/new", methods=['GET', 'POST'])
    def url_visit_new():
        form = VisitForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = Visit()
            o.datum = form.datum.data
            o.information = form.information.data
            db.session.add(o)
            db.session.commit()
            return redirect(url_for('url_visit_index'))
        page_info = WebPageContent("petclinic_visit", "new")
        return render_template(
            "petclinic_model/visit/new.html",
            form=form,
            page_info=page_info
        )

    @staticmethod
    @app.route("/vet")
    def url_vet_index(page=1):
        page_info = WebPageContent("petclinic_vet", "index")
        page_data = Vet.get_all(page)
        return render_template(
            "petclinic_model/vet/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/vet/new", methods=['GET', 'POST'])
    def url_vet_new():
        form = VetForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = Vet()
            o.first_name = form.first_name.data
            o.last_name = form.last_name.data
            db.session.add(o)
            db.session.commit()
            return redirect(url_for('url_vet_index'))
        page_info = WebPageContent("petclinic_vet", "new")
        return render_template(
            "petclinic_model/vet/new.html",
            form=form,
            page_info=page_info
        )

    @staticmethod
    @app.route("/specialty")
    def url_specialty_index(page=1):
        page_info = WebPageContent("petclinic_specialty", "index")
        page_data = Specialty.get_all(page)
        return render_template(
            "petclinic_model/specialty/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/specialty/new", methods=['GET', 'POST'])
    def url_specialty_new():
        form = SpecialtyForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = Specialty()
            o.name = form.name.data
            db.session.add(o)
            db.session.commit()
            return redirect(url_for('url_specialty_index'))
        page_info = WebPageContent("petclinic_specialty", "new")
        return render_template(
            "petclinic_model/specialty/new.html",
            form=form,
            page_info=page_info
        )


domain_model_urls = DomainModelUrls()
