import os
import psycopg2

DB_NAME = 'messages_server_db'
DB_URI = os.environ.get('SERVER_DB_URI')  # postgresql://postgres@localhost
DB_COMPLETE_URI = '/'.join((DB_URI, DB_NAME))


def nuke_db(db_name=DB_NAME, db_uri=DB_URI):
    with psycopg2.connect(db_uri) as cnx:
        cnx.autocommit = True
        sql = f"DROP DATABASE {db_name}"
        with cnx.cursor() as curs:
            curs.execute(sql)


def create_db(db_name=DB_NAME, db_uri=DB_URI):
    with psycopg2.connect(db_uri) as cnx:
        cnx.autocommit = True
        sql = f"CREATE DATABASE {db_name}"
        with cnx.cursor() as curs:
            curs.execute(sql)


def create_table_users(db_uri=DB_COMPLETE_URI):
    sql = """CREATE TABLE Users(
        id SERIAL,
        username VARCHAR(255) NOT NULL UNIQUE,
        email VARCHAR(255) UNIQUE, 
        hashed_password VARCHAR(80) NOT NULL,
        PRIMARY KEY (id)
        )"""
    with psycopg2.connect(db_uri) as cnx:
        with cnx.cursor() as curs:
            curs.execute(sql)


def create_table_messages(db_uri=DB_COMPLETE_URI):
    sql = """CREATE TABLE Messages(
        id SERIAL,
        from_id INTEGER NOT NULL,
        to_id INTEGER NOT NULL,
        msg_text TEXT,
        creation_date TIMESTAMP NOT NULL DEFAULT NOW(),
        PRIMARY KEY (id),
        FOREIGN KEY (from_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (to_id) REFERENCES users(id) ON DELETE CASCADE
        )"""
    with psycopg2.connect(db_uri) as cnx:
        with cnx.cursor() as curs:
            curs.execute(sql)


if __name__ == '__main__':
    nuke_db()
    create_db()
    create_table_users()
    create_table_messages()
    pass
