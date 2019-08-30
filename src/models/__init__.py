import psycopg2
from psycopg2.extras import RealDictCursor

DB_NAME = 'msg_server_db'
DB_URI = 'postgresql://postgres@localhost'
COMPLETE_DB_URI = 'postgresql://postgres@localhost/msg_server_db'


def nuke_db(db_name=DB_NAME, db_uri=DB_URI):
    with psycopg2.connect(db_uri) as cnx:
        cnx.autocommit = True
        sql = "DROP DATABASE " + db_name
        with cnx.cursor() as curs:
            try:
                curs.execute(sql)
                print('DB nuked!')
            except psycopg2.ProgrammingError:
                print('DB do not exist')


def create_db(db_name=DB_NAME, db_uri=DB_URI):
    with psycopg2.connect(db_uri) as cnx:
        cnx.autocommit = True
        sql = f"CREATE DATABASE {db_name}"
        with cnx.cursor() as curs:
            curs.execute(sql)
            print('DB created!')


def create_table_users(db_uri=COMPLETE_DB_URI):
    sql = """CREATE TABLE Users(
        id SERIAL,
        username VARCHAR(255) NOT NULL UNIQUE,
        hashed_password VARCHAR(80) NOT NULL,
        PRIMARY KEY (id)
        )"""
    with psycopg2.connect(db_uri) as cnx:
        with cnx.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(sql)
            print('Table users created!')


def create_table_messages(complete_db_uri=COMPLETE_DB_URI):
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
    with psycopg2.connect(complete_db_uri) as cnx:
        with cnx.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(sql)
            print('Table messages created!')


if __name__ == '__main__':
    nuke_db()
    create_db()
    create_table_users()
    create_table_messages()
    pass
