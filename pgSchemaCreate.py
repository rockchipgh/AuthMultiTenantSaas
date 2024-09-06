import psycopg2

conn = psycopg2.connect(database='postgres',
                        user='postgres',
                        host='localhost',
                        password='root',
                        port=5432)
conn.autocommit = True
cur = conn.cursor()
sql = 'CREATE DATABASE UAT;'
try:
    cur.execute(sql)
except psycopg2.errors.DuplicateDatabase:
    print("Database already exists")
except:
    print("Unknown Error while creating database")


conn.close()