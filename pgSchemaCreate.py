import yaml
import psycopg2

def load_yaml(filename):
    with open(filename) as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config

def create_database(config, db='postgres'):
    conn = psycopg2.connect(database=db,
                            user=config['postgres']['user'],
                            host=config['postgres']['host'],
                            password=config['postgres']['password'],
                            port=config['postgres']['port'])
    conn.autocommit = True
    cur = conn.cursor()
    sql = f"CREATE DATABASE {config['postgres']['database']};"
    try:
        cur.execute(sql)
    except psycopg2.errors.DuplicateDatabase:
        print("Database already exists")
    except:
        print("Unknown Error while creating database")
    conn.close()

def create_schema(config):
    conn = psycopg2.connect(database=config['postgres']['database'],
                        user=config['postgres']['user'],
                        host=config['postgres']['host'],
                        password=config['postgres']['password'],
                        port=config['postgres']['port'])
    conn.autocommit = True

    cur = conn.cursor()
    sql = '''
    CREATE SCHEMA IF NOT EXISTS uat;

    CREATE TABLE uat.organisation (
        id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
        name VARCHAR(255) NOT NULL,
        status INT DEFAULT 0 NOT NULL,
        personal boolean default FALSE,
        settings JSON default '{}',
        created_at BIGINT, 
        updated_at BIGINT
    );

    CREATE TABLE uat."user" (
        id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        profile JSON DEFAULT '{}' NOT NULL,
        status INT DEFAULT 0 NOT NULL,
        settings JSON default '{}' NOT NULL,
        created_at BIGINT, 
        updated_at BIGINT
    );


    CREATE TABLE uat."role" (
        id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
        name VARCHAR(255) NOT NULL,
        description VARCHAR(255),
        org_id INT NOT NULL, 
        CONSTRAINT fk_key1
            FOREIGN KEY(org_id)
            REFERENCES uat.organisation(id) 
            ON DELETE CASCADE
    );

    CREATE TABLE uat."member" (
        org_id INT NOT NULL,
        user_id INT NOT NULL,
        role_id INT NOT NULL,
        status INT DEFAULT 0 NOT NULL,
        settings JSON default '{}' NOT NULL,
        created_at BIGINT, 
        updated_at BIGINT,
        CONSTRAINT fk_key1
            FOREIGN KEY(org_id)
            REFERENCES uat.organisation(id) 
            ON DELETE CASCADE,
        CONSTRAINT fk_key2
            FOREIGN KEY(user_id)
            REFERENCES uat."user"(id) 
            ON DELETE CASCADE,
        CONSTRAINT fk_key3
            FOREIGN KEY(role_id)
            REFERENCES uat.role(id) 
            ON DELETE CASCADE
    );

    '''
    cur.execute(sql)
    conn.close()

def load_examples(config):
    conn = psycopg2.connect(database=config['postgres']['database'],
                        user=config['postgres']['user'],
                        host=config['postgres']['host'],
                        password=config['postgres']['password'],
                        port=config['postgres']['port'])
    conn.autocommit = True

    cur = conn.cursor()
    sql = '''
    INSERT INTO uat.organisation (name, status, personal, settings, created_at, updated_at) VALUES
    ('Tech Corp', 1, FALSE, '{"theme": "dark", "notifications": "enabled"}', 1693899600000, 1694909600000),
    ('Health Solutions', 1, FALSE, '{"theme": "light", "notifications": "disabled"}', 1693899600000, 1694909600000),
    ('Education First', 1, TRUE, '{"theme": "blue", "notifications": "enabled"}', 1693899600000, 1694909600000);

    INSERT INTO uat."user" (email, password, profile, status, settings, created_at, updated_at) VALUES
    ('john.doe@example.com', 'hashed_password1', '{"name": "John Doe", "age": 30}', 1, '{"lang": "en"}', 1693899600000, 1694909600000),
    ('jane.smith@example.com', 'hashed_password2', '{"name": "Jane Smith", "age": 25}', 1, '{"lang": "en"}', 1693899600000, 1694909600000),
    ('admin@example.com', 'hashed_password3', '{"name": "Admin User", "age": 35}', 1, '{"lang": "en"}', 1693899600000, 1694909600000);

    INSERT INTO uat."role" (name, description, org_id) VALUES
    ('Admin', 'Admin role with full permissions', 1),
    ('Manager', 'Manager role with limited permissions', 1),
    ('Employee', 'Employee role with basic access', 2);

    INSERT INTO uat."member" (org_id, user_id, role_id, status, settings, created_at, updated_at) VALUES
    (1, 1, 1, 1, '{"permissions": "all"}', 1693899600000, 1694909600000),
    (1, 2, 2, 1, '{"permissions": "manage_users"}', 1693899600000, 1694909600000),
    (2, 2, 3, 1, '{"permissions": "basic_access"}', 1693899600000, 1694909600000);


    '''
    cur.execute(sql)
    conn.close()


config = load_yaml("config.yaml")
create_database(config)
create_schema(config)
load_examples(config)