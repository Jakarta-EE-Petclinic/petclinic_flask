# PostgreSQL

## create user

````PostgreSQL
    CREATE ROLE petclinic_flask WITH
        LOGIN
        SUPERUSER
        CREATEDB
        CREATEROLE
        INHERIT
        REPLICATION
        CONNECTION LIMIT -1
        PASSWORD 'petclinic_flask';

    GRANT pg_execute_server_program, pg_monitor, pg_read_all_settings,
        pg_read_all_stats, pg_read_server_files, pg_signal_backend
    TO flask_petclinic
        WITH ADMIN OPTION;
````

## create tablespace

````PostgreSQL
    CREATE TABLESPACE tablespace_petclinic_flask
      OWNER flask_petclinic
      LOCATION '/opt/postgresql/tablespace_petclinic_flask';

    ALTER TABLESPACE tablespace_petclinic_flask
      OWNER TO petclinic_flask;
````

## create database

petclinic_flask

````PostgreSQL
    CREATE DATABASE petclinic_flask
        WITH
        OWNER = petclinic_flask
        TEMPLATE = template0
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_petclinic
        CONNECTION LIMIT = -1;
````

flask_petclinic_testing

````PostgreSQL
    CREATE DATABASE petclinic_flask_testing
        WITH
        OWNER = petclinic_flask
        TEMPLATE = petclinic_flask
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_petclinic_flask
        CONNECTION LIMIT = -1;
````
