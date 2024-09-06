import yaml
import psycopg2

with open("config.yaml") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

conn = psycopg2.connect(database='postgres',
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

conn = psycopg2.connect(database='postgres',
                        user=config['postgres']['user'],
                        host=config['postgres']['host'],
                        password=config['postgres']['password'],
                        port=config['postgres']['port'])
conn.autocommit = True
cur = conn.cursor()

