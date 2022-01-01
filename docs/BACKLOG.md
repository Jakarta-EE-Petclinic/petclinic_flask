# BACKLOG

## Use Cases

### Matrix Data Blueprints for Use Cases

## Test Cases

## Milestones and their Issues

## Releases via Milestones and their Issues

### 0.0.1 Release

* Fixed #1 test 1 2 3

### 0.0.2 Release

* Fixed #2 start data update job via web ui
* Fixed #4 data update: who_country

### 0.0.3 Release

* Fixed #8 view_who_today_new_deaths
* Fixed #9 view_who_global_data

### 0.0.4 Release

* Fixed #13 Pagination for all Tables
* Fixed #14 Running on Windows and Linux
* Fixed #15 Navigation: Region, Countries, Data per Countries order by Date

### 0.0.5 Release

* Fixed #1 Async Tasks for import and update Data with Celery and RabbitMQ
* Fixed #2 Move Repo to github

### 0.0.6 Release

* Fixed #6 data of all reported countries for WHO date reported
* Fixed #7 WHO Countries all - data for Country

### 0.0.7 Release

* Issue #8 WhoServiceUpdate.update_db_short()
* Issue #9 URL: /who/update/short

### 0.0.8 Release

* Fixed #13 /who/imported/
* Fixed #14 /europe/imported/
* Fixed #21 better templates for who_global_data tables

### 0.0.9 Release

* Fixed #18 /europe/update: Download
* Fixed #19 /europe/update: Import File to DB
* Fixed #20 /europe/update: Update DB

### 0.0.10 Release

* Fixed #24 update_data
* Fixed #29 /who/info
* Fixed #30 /europa/info

### 0.0.11 Release

* Fixed #26 /admin/database/dump
* Fixed #43 /europe/date_reported

### 0.0.12 Release

* Fixed #55 /vaccination/tasks
* Fixed #56 /vaccination/info

### 0.0.13 Release

* Fixed #49 EcdcServiceUpdate.__update_data_short() (wontfix)
* Fixed #52 download vaccination timeline data file

### 0.0.14 Release

* Fixed #69 Branch: ISSUE_66_ATTEMPT_01
* Fixed #70 load package.json from Bootstrap-Template sb-admin-angular into statics

### 0.0.15 Release

* Fixed #88 rename VaccinationImport to VaccinationImport
* Fixed #89 change tablename from vaccination_germany_timeline_import to vaccination_import

* Fixed #87 change to: Vaccination.datum many to one VaccinationDateReported
* Fixed #106 add Tasks and URLs for starting Tasks to vaccination_views

### 0.0.16 Release

* Fixed #111 refactor to new method scheme introduced 07.02.2021
* Fixed #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021

### 0.0.17 Release

* Fixed #82 change to ORM ClassHierarchy
* Fixed #42 SQLalchemy instead of SQL: OwidImport.get_new_dates_as_array()

### 0.0.18 Release

* Fixed #133 implement RkiBundeslaenderService.task_database_drop_create
* Fixed #134 implement RkiBundeslaenderService.run_update_dimension_tables_only

### 0.0.19 Release

### 0.0.20 Release

### 0.0.21 Release

### 0.0.22 Release

### 0.0.23 Release

### 0.0.24 Release

* Fixed #28 /admin/database/import
* Fixed #66 frontend: migrate to Bootstrap Theme sb-admin-angular
* Fixed #158 load Bootstrap-Template sb-admin-angular into static

### 0.0.25 Release

* Fixed #158 load Bootstrap-Template sb-admin-angular into static

### 0.0.26 Release

* Fixed #194 dependency is unsecure

### 0.0.27 Release

* Fixed #60 frontend: better design for tables
* Fixed #62 frontend: better design for pages

### 0.0.28 Release

* Fixed #199 Database export without gzip
* Fixed #200 Database import without gzip

### 0.0.29 Release

* Fixed #201 UML: blueprint user
* Fixed #205 navbar is broken

### 0.0.30 Release

* Fixed #206 implement user login and authorization using blueprint user and flask-login

### 0.0.31 Release

* Fixed #211 ECDC-templates: change URL to for_url()
* Fixed #213 WHO-template: change URL to for_url()

### 0.0.32 Release

* Fixed #212 implement OwidService.task_database_drop_create()
* Fixed #214 implement OwidServiceUpdate.update_dimension_tables_only()

### 0.0.33 Release

* Fixed #165 implement url_ecdc_task_download_only in europe_views.py
* Fixed #166 implement url_ecdc_task_import_only in europe_views.py

### 0.0.34 Release

* Fixed #225 Add Issue Matrix to Gitlab

### 0.0.35 Release

* Fixed #314 RKI Data Import and full update
* Fixed #315 Data Import into Flat-Table for OWID, RKI, ECDC, WHO
* Fixed #316 Refactoring to simplify structure

### 0.0.36 Release

* Issue #195 VaccinationImport.get_daterep_missing_in_vaccination_data(): native SQL to SQLalechemy Query
* Issue #317 BUG: Vaccination Data Import and full update

### WHO

* Issue #226 WHO: Development: Navigation and Pages for Info, Tasks and Tests
* Issue #227 WHO: Development: Download Data File
* Issue #228 WHO: Development: import

### OWID

* Issue #243 OWID: Development: Navigation and Pages for Info, Tasks and Tests
* Issue #244 OWID: Development: Download Data File
* Issue #245 OWID: Development: import
* Issue #246 OWID: Development: import_flat

### ECDC

* Issue #259 ECDC: Development: Navigation and Pages for Info, Tasks and Tests
* Issue #260 ECDC: Development: Download Data File
* Issue #261 ECDC: Development: import
* Issue #262 ECDC: Development: import_flat

### RKI Vaccination

* Issue #274 RKI Vaccination: Development: Navigation and Pages for Info, Tasks and Tests
* Issue #275 RKI Vaccination: Development: Download Data File

### Vaccination: Development: Navigation and Pages for Fact Table

* Issue #285 RKI Vaccination: Documentation: Update UML Diagrams for Domain Model
* Issue #286 RKI Vaccination: Documentation: Update UML Diagrams for Use Cases

### RKI

* Issue #291 RKI: Development: Navigation and Pages for Info, Tasks and Tests
* Issue #292 RKI: Development: Download Data File
* Issue #293 RKI: Development: import

### 0.0.39 Release

* Issue #220 add Selenium Tests for all Frontend Urls and Pages without any Access to Database
* Issue #221 add Selenium Tests for all Frontend Urls and Pages with Read Access to Database

### 0.0.38 Release

* Issue #195 VaccinationImport.get_daterep_missing_in_vaccination_data(): native SQL to SQLalechemy Query

* Issue #207 remove deprecated: database.port
* Issue #208 remove deprecated: database.run_run_with_debug
* Issue #209 remove deprecated: database.ITEMS_PER_PAGE

### 0.0.37 Release

* Issue #195 VaccinationImport.get_daterep_missing_in_vaccination_data(): native SQL to SQLalechemy Query


### 00 Inbox

* Issue add Selenium Tests for all Frontend Urls and Pages without any Access to Database
* Issue add Selenium Tests for all Frontend Urls and Pages with Read Access to Database

### 01 Next

* Issue #198 UML: WHO Visual Graphs for Data per Countries order by Date
* Issue #5 WHO Visual Graphs for Data per Countries order by Date


### 02 Soon

* Issue #189 setup unit tests
* Issue #190 setup docs with sphinx

### 03 Nice to Have

* Issue #59 frontend: add correct breadcrumb to every page
* Issue #61 frontend: better design for navtabs
* Issue #63 frontend: add footer design

### 04 Dropped

* Issue #185 add Flask-Redisboard
* Issue #186 add Flask-Monitoring

### 05 Later maybe

* Issue #180 add build.cmd script
* Issue #181 add flask-filealchemy

### 06 BUGS Frontend
