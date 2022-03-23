.. petclinic_flask documentation master file, created by
   sphinx-quickstart on Thu Dec  9 20:44:03 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to petclinic_flask's documentation!
===========================================

.. sqla-model:: project.app_web.notification.Notification
.. sqla-model:: project.app_web.project.app_web.user.User
.. sqla-model:: project.petclinic_model.owner.Owner
.. sqla-model:: project.petclinic_model.pet.Pet
.. sqla-model:: project.petclinic_model.pettype.PetType
.. sqla-model:: project.petclinic_model.specialty.Specialty
.. sqla-model:: project.petclinic_model.vet.Vet
.. sqla-model:: project.petclinic_model.visit.Visit

.. uml:: ../project/petclinic_model/entities/entities.puml
.. uml:: ../project/app_web/entities/entities.puml
.. uml:: ../project/app_web/cms/cms_transient.puml
.. uml:: ../project/app_web/notification/notification.puml
.. uml:: ../project/app_web/user/user.puml
.. uml:: ../project/app_web/services/services.puml

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   README.md
   UML.md
   CHANGES.md
   TODO.md
   SETUP_DEV_ENV.md
   db/MariadDB.md
   db/PostgresSQL.md
   db/postgresql/pgpass.txt

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
