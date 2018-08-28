from psycopg2 import connect
from psycopg2.extras import DictCursor


def db_connect(username, passwd, hostname):
    db_name = 'messages_server_db'
    cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
    curs = cnx.cursor(cursor_factory=DictCursor)
    return curs
