import flask
from flask import Blueprint, request, flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.collections import InstrumentedList

from project.app_config.database import app, db, login_manager

from project.app_web.user import LoginForm, User, UserService
from project.app_web.cms_transient import WebPageContent
from project.app_web.services import AdminService
from project.app_web.notification import Notification, NotificationService

from project.petclinic_model.owner import Owner, OwnerNewForm, OwnerShowForm, \
    OwnerEditForm, OwnerService
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
    def url_all_notification():
        page = request.args.get('page', 1, type=int)
        page_info = WebPageContent("All", "Notifications")
        page_data = Notification.notifications_get(page)
        return render_template(
            "app_notification/notification/app_all_notification.html",
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app.route("/notification/read")
    @login_required
    def url_all_notification_mark_read():
        page = request.args.get('page', 1, type=int)
        page_data = Notification.notifications_get(page)
        for o in page_data.items:
            o.read()
            db.session.add(o)
        db.session.commit()
        return redirect(url_for("url_all_notification", page=page))

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


class DomainModelOwnerUrls:
    """
    .. uml:: petclinic_model/entities.uml
    .. uml:: petclinic_model/owner.uml
    """
    def __init__(self):
        app.logger.info(" DomainModelOwnerUrls [init]")

    @staticmethod
    @app.route("/owner/search")
    def url_owner_search():
        """usecase owner_search as uc6000"""
        searchterm = request.args.get('searchterm', '', type=str)
        page_info = WebPageContent("petclinic_owner", "search")
        page_data = Owner.search(searchterm)
        return render_template(
            "petclinic_model/owner/owner_index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/owner")
    def url_owner_index():
        """usecase owner_list as uc6001"""
        page = request.args.get('page', 1, type=int)
        page_info = WebPageContent("petclinic_owner", "index")
        page_data = Owner.get_all(page)
        return render_template(
            "petclinic_model/owner/owner_index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/owner/new", methods=['GET', 'POST'])
    def url_owner_new():
        """usecase owner_new as uc6003"""
        form = OwnerNewForm()
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
            flash("saved new Owner "+o.__str__())
            return redirect(url_for('url_owner_index'))
        else:
            page_info = WebPageContent("petclinic_owner", "new")
            return render_template(
                "petclinic_model/owner/owner_new.html",
                form=form,
                page_info=page_info
            )

    @staticmethod
    @app.route("/owner/<int:owner_id>")
    def url_owner_show(owner_id: int):
        """usecase owner_change as uc6002"""
        page_info = WebPageContent("petclinic_owner", "show")
        form = OwnerShowForm()
        o = Owner.find_by_id(owner_id)
        form.first_name.data = o.first_name
        form.last_name.data = o.last_name
        form.street_address.data = o.street_address
        form.zip_code.data = o.zip_code
        form.city.data = o.city
        form.telephone.data = o.telephone
        form.email.data = o.email
        return render_template(
            "petclinic_model/owner/owner_show.html",
            owner=o,
            form=form,
            owner_id=owner_id,
            page_info=page_info
        )

    @staticmethod
    @app.route("/owner/<int:owner_id>/edit", methods=['GET', 'POST'])
    def url_owner_edit(owner_id: int):
        """owner_change as uc6002"""
        page_info = WebPageContent("petclinic_owner", "edit")
        form = OwnerEditForm()
        o = Owner.find_by_id(owner_id)
        if request.method == 'POST' and form.validate_on_submit():
            o.first_name = form.first_name.data
            o.last_name = form.last_name.data
            o.street_address = form.street_address.data
            o.zip_code = form.zip_code.data
            o.city = form.city.data
            o.telephone = form.telephone.data
            o.email = form.email.data
            db.session.add(o)
            db.session.commit()
            flash("saved edited Owner "+o.__str__())
            return redirect(url_for('url_owner_shows', owner_id=owner_id))
        else:
            form.first_name.data = o.first_name
            form.last_name.data = o.last_name
            form.street_address.data = o.street_address
            form.zip_code.data = o.zip_code
            form.city.data = o.city
            form.telephone.data = o.telephone
            form.email.data = o.email
            return render_template(
                "petclinic_model/owner/owner_edit.html",
                owner_id=owner_id,
                form=form,
                page_info=page_info
            )

    @staticmethod
    @app.route("/owner/<int:owner_id>/pet/add", methods=['GET', 'POST'])
    def url_owner_pet_add(owner_id: int):
        """usecase owner_add_new_pet as uc6004"""
        form = OwnerEditForm()
        o = Owner.find_by_id(owner_id)
        return redirect(url_for('url_owner_index'))

    @staticmethod
    @app.route("/owner/<int:owner_id>/pet/<int:pet_id>", methods=['GET', 'POST'])
    def url_owner_pet_change(owner_id: int, pet_id: int):
        """usecase owner_change_pet as uc6005"""
        form = OwnerEditForm()
        o = Owner.find_by_id(owner_id)
        return redirect(url_for('url_owner_index'))

    @staticmethod
    @app.route("/owner/<int:owner_id>/pet/<int:pet_id>/remove", methods=['GET', 'POST'])
    def url_owner_remove_pet(owner_id: int, pet_id: int):
        """usecase owner_remove_pet as uc6006"""
        form = OwnerEditForm()
        o = Owner.find_by_id(owner_id)
        return redirect(url_for('url_owner_index'))

    @staticmethod
    @app.route("/owner/<int:owner_id>/pet/<int:pet_id>/transfer-ownership", methods=['GET', 'POST'])
    def url_owner_give_pet_to_another_owner(owner_id: int, pet_id: int):
        """usecase owner_give_pet_to_another_owner as uc6007"""
        form = OwnerEditForm()
        o = Owner.find_by_id(owner_id)
        return redirect(url_for('url_owner_index'))


domain_model_owner_urls = DomainModelOwnerUrls()


class DomainModelPetUrls:
    """
    .. uml:: petclinic_model/entities.uml
    .. uml:: petclinic_model/pet.uml
    """
    def __init__(self):
        app.logger.info(" DomainModelPetUrls [init]")

    @staticmethod
    @app.route("/pet/search")
    def url_pet_search():
        """usecase pet_search as uc5000"""
        searchterm = request.args.get('searchterm', '', type=str)
        page_info = WebPageContent("petclinic_owner", "search")
        page_data = Owner.search(searchterm)
        return render_template(
            "petclinic_model/pet/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/pet")
    def url_pet_index():
        """usecase pet_list as uc5001"""
        page = request.args.get('page', 1, type=int)
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
        """usecase pet_new as uc5002"""
        form = PetForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = Pet()
            o.name = form.name.data
            o.date_of_birth = form.date_of_birth.data
            o.owner = form.owner_select.data
            o.pettype = form.pettype_select.data
            db.session.add(o)
            db.session.commit()
            flash("saved edited Owner "+o.__str__())
            return redirect(url_for('url_pet_index'))
        else:
            page_info = WebPageContent("petclinic_pet", "new")
            return render_template(
                "petclinic_model/pet/new.html",
                form=form,
                page_info=page_info
            )

    @staticmethod
    @app.route("/pet/<pet_id>", methods=['GET', 'POST'])
    def url_pet_show():
        """usecase pet_new as uc5002"""
        pass

    @staticmethod
    @app.route("/pet/<pet_id>/edit", methods=['GET', 'POST'])
    def url_pet_edit():
        """usecase pet_change as uc5003"""
        pass

    @staticmethod
    @app.route("/pet/<pet_id>/remove", methods=['GET', 'POST'])
    def url_pet_remove():
        """usecase pet_remove as uc5004"""
        pass

domain_model_pet_urls = DomainModelPetUrls()


class DomainModelVisitUrls:
    """
    .. uml:: petclinic_model/entities.uml
    .. uml:: petclinic_model/visit.uml
    """
    def __init__(self):
        app.logger.info(" DomainModelVisitUrls [init]")

    @staticmethod
    @app.route("/visit/search")
    def url_visit_search():
        """ usecase visit_search as uc7000"""
        searchterm = request.args.get('searchterm', '', type=str)
        page_info = WebPageContent("petclinic_visit", "search")
        page_data = Visit.search(searchterm)
        return render_template(
            "petclinic_model/visit/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/visit")
    def url_visit_index():
        """usecase visit_list as uc7001"""
        page = request.args.get('page', 1, type=int)
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
        """usecase visit_new as uc7002"""
        form = VisitForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = Visit()
            o.datum = form.datum.data
            o.information = form.information.data
            o.pet = form.pet_select.data
            db.session.add(o)
            db.session.commit()
            return redirect(url_for('url_visit_index'))
        else:
            page_info = WebPageContent("petclinic_visit", "new")
            return render_template(
                "petclinic_model/visit/new.html",
                form=form,
                page_info=page_info
            )

    @staticmethod
    @app.route("/visit/<pet_id>", methods=['GET', 'POST'])
    def url_visit_show():
        """usecase visit_show as uc7003"""
        pass

    @staticmethod
    @app.route("/visit/<pet_id>/edit", methods=['GET', 'POST'])
    def url_visit_edit():
        """usecase visit_change as uc7004"""
        pass

    @staticmethod
    @app.route("/visit/<pet_id>/remove", methods=['GET', 'POST'])
    def url_visit_remove():
        """usecase visit_remove as uc7005"""
        pass


domain_model_visit_urls = DomainModelVisitUrls()


class DomainModelPetTypeUrls:
    """
    .. uml:: petclinic_model/entities.uml
    .. uml:: petclinic_model/pettype.uml
    """
    def __init__(self):
        app.logger.info(" DomainModelPetTypeUrls [init]")


    @staticmethod
    @app.route("/pettype/search")
    def url_pettype_search():
        """usecase pettype_search as uc4000"""
        searchterm = request.args.get('searchterm', '', type=str)
        page_info = WebPageContent("petclinic_pettype", "search")
        page_data = Owner.search(searchterm)
        return render_template(
            "petclinic_model/owner/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/pettype")
    def url_pettype_index():
        """usecase pettype_list as uc4001"""
        page = request.args.get('page', 1, type=int)
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
        """usecase pettype_new as uc4002"""
        form = PetTypeForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = PetType()
            o.name = form.name.data
            db.session.add(o)
            db.session.commit()
            flash("saved new PetType "+o.__str__())
            return redirect(url_for('url_pettype_index'))
        else:
            page_info = WebPageContent("petclinic_pettype", "new")
            return render_template(
                "petclinic_model/pettype/new.html",
                form=form,
                page_info=page_info
            )

    @staticmethod
    @app.route("/pettype/<int:pettype_id>/show", methods=['GET', 'POST'])
    def url_pettype_show(pettype_id: int):
        """usecase pettype_change as uc4003"""
        form = PetTypeForm()
        o = PetType.find_by_id(pettype_id)
        form.name.data = o.name
        page_info = WebPageContent("petclinic_pettype", "show")
        return render_template(
            "petclinic_model/pettype/show.html",
            form=form,
            pettype_id=pettype_id,
            page_info=page_info
        )

    @staticmethod
    @app.route("/pettype/<int:pettype_id>/edit", methods=['GET', 'POST'])
    def url_pettype_change(pettype_id: int):
        """usecase pettype_change as uc4003"""
        form = PetTypeForm()
        o = PetType.find_by_id(pettype_id)
        if request.method == 'POST' and form.validate_on_submit():
            o.name = form.name.data
            db.session.add(o)
            db.session.commit()
            flash("saved changed PetType "+o.__str__())
            return redirect(url_for('url_pettype_index'))
        else:
            form.name.data = o.name
            page_info = WebPageContent("petclinic_pettype", "edit")
            return render_template(
                "petclinic_model/pettype/edit.html",
                form=form,
                pettype_id=pettype_id,
                page_info=page_info
            )

    @staticmethod
    @app.route("/pettype/<int:pettype_id>/remove", methods=['GET', 'POST'])
    def url_pettype_remove(pettype_id: int):
        """usecase pettype_remove as uc4004"""
        pass


domain_model_pettype_urls = DomainModelPetTypeUrls()


class DomainModelVetUrls:
    """
    .. uml:: petclinic_model/entities.uml
    .. uml:: petclinic_model/vet.uml
    """
    def __init__(self):
        app.logger.info(" DomainModelVetUrls [init]")

    @staticmethod
    @app.route("/vet/search")
    def url_vet_search():
        """usecase vet_search as uc3000"""
        searchterm = request.args.get('searchterm', '', type=str)
        page_info = WebPageContent("petclinic_vet", "search")
        page_data = Vet.search(searchterm)
        return render_template(
            "petclinic_model/vet/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/vet")
    def url_vet_index():
        """usecase vet_list as uc3001"""
        page = request.args.get('page', 1, type=int)
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
        """usecase vet_new as uc3002"""
        form = VetForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = Vet()
            o.first_name = form.first_name.data
            o.last_name = form.last_name.data
            o.specialities.clear()
            for s in form.specialty_select.data:
                o.specialities.append(s)
            db.session.add(o)
            db.session.commit()
            flash("saved news Vet "+o.__str__())
            return redirect(url_for('url_vet_index'))
        else:
            page_info = WebPageContent("petclinic_vet", "new")
            return render_template(
                "petclinic_model/vet/new.html",
                form=form,
                page_info=page_info
            )

    @staticmethod
    @app.route("/vet/show", methods=['GET', 'POST'])
    def url_vet_show():
        """usecase vet_show as uc3003"""
        pass

    @staticmethod
    @app.route("/vet/<int:vet_id>/edit", methods=['GET', 'POST'])
    def url_vet_change(vet_id: int):
        """usecase vet_change as uc3004"""
        form = VetForm()
        o = Vet().find_by_id(vet_id)
        if request.method == 'POST' and form.validate_on_submit():
            o.first_name = form.first_name.data
            o.last_name = form.last_name.data
            o.specialities.clear()
            for s in form.specialty_select.data:
                o.specialities.append(s)
            db.session.add(o)
            db.session.commit()
            flash("saved changed Vet "+o.__str__())
            return redirect(url_for('url_vet_index'))
        else:
            form.first_name.data = o.first_name
            form.last_name.data = o.last_name
            form.specialty_select.data = o.specialities
            page_info = WebPageContent("petclinic_vet", "edit")
            return render_template(
                "petclinic_model/vet/new.html",
                form=form,
                page_info=page_info
            )

    @staticmethod
    @app.route("/vet/remove", methods=['GET', 'POST'])
    def url_vet_remove():
        """usecase vet_remove as uc3006"""
        pass


domain_model_vet_urls = DomainModelVetUrls()


class DomainModelSpecialtyUrls:
    """
    .. uml:: petclinic_model/entities.uml
    .. uml:: petclinic_model/specialty.uml
    """
    def __init__(self):
        app.logger.info(" DomainModelSpecialtyUrls [init]")

    @staticmethod
    @app.route("/specialty/search")
    def url_specialty_search():
        """usecase specialty_search as uc2000"""
        searchterm = request.args.get('searchterm', '', type=str)
        page_info = WebPageContent("petclinic_specialty", "search")
        page_data = Specialty.search(searchterm)
        return render_template(
            "petclinic_model/specialty/index.html",
            page_data=page_data,
            page_info=page_info
        )

    @staticmethod
    @app.route("/specialty")
    def url_specialty_index():
        """usecase specialty_list as uc2001"""
        page = request.args.get('page', 1, type=int)
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
        """usecase specialty_new as uc2002"""
        form = SpecialtyForm()
        if request.method == 'POST' and form.validate_on_submit():
            o = Specialty()
            o.name = form.name.data
            db.session.add(o)
            db.session.commit()
            flash("saved new Specialty "+o.__str__())
            return redirect(url_for('url_specialty_index'))
        else:
            page_info = WebPageContent("petclinic_specialty", "new")
            return render_template(
                "petclinic_model/specialty/new.html",
                form=form,
                page_info=page_info
            )

    @staticmethod
    @app.route("/specialty/<int:specialty_id>", methods=['GET', 'POST'])
    def url_specialty_show(specialty_id: int):
        """usecase specialty_show as uc2003"""
        o = Specialty.find_by_id(specialty_id)
        form = SpecialtyForm()
        if request.method == 'POST' and form.validate_on_submit():
            o.name = form.name.data
            db.session.add(o)
            db.session.commit()
            flash("saved changed Specialty "+o.__str__())
            return redirect(url_for('url_specialty_index'))
        else:
            page_info = WebPageContent("url_specialty_show", "show")
            form.name.data = o.name
            return render_template(
                "petclinic_model/specialty/show.html",
                form=form,
                page_info=page_info
            )

    @staticmethod
    @app.route("/specialty/remove", methods=['GET', 'POST'])
    def url_specialty_remove():
        """usecase specialty_remove as uc2005"""
        pass


domain_model_specialty_urls = DomainModelSpecialtyUrls()
