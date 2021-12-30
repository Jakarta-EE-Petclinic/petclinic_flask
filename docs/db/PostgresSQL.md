# PostgreSQL

## create user

````PostgreSQL
    CREATE ROLE flask_petclinic WITH
        LOGIN
        SUPERUSER
        CREATEDB
        CREATEROLE
        INHERIT
        REPLICATION
        CONNECTION LIMIT -1
        PASSWORD 'flask_petclinicpwd';

    GRANT pg_execute_server_program, pg_monitor, pg_read_all_settings,
        pg_read_all_stats, pg_read_server_files, pg_signal_backend
    TO flask_petclinic
        WITH ADMIN OPTION;
````

## create tablespace

````PostgreSQL
    CREATE TABLESPACE tablespace_flask_petclinic
      OWNER flask_petclinic
      LOCATION '/opt/postgresql/tablespace_flask_petclinic';

    ALTER TABLESPACE tablespace_flask_petclinic
      OWNER TO flask_petclinic;
````

## create database

flask_petclinic

````PostgreSQL
    CREATE DATABASE flask_petclinic
        WITH
        OWNER = flask_petclinic
        TEMPLATE = template0
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_petclinic
        CONNECTION LIMIT = -1;
````

flask_petclinic_testing

````PostgreSQL
    CREATE DATABASE flask_petclinic_testing
        WITH
        OWNER = flask_petclinic
        TEMPLATE = flask_petclinic
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_petclinic
        CONNECTION LIMIT = -1;
````
