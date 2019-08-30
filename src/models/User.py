import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
from . import COMPLETE_DB_URI


class User:
    __id = None
    username = None
    __hashed_password = None

    def __init__(self):
        self.__id = -1
        self.username = ''
        self.__hashed_password = ''

    def __str__(self):
        return f"User | id: {self.id} | username: {self.username}"

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    @hashed_password.setter
    def hashed_password(self, password):
        if len(password) >= 8:
            self.__hashed_password = str(User.hash_password(password), 'utf-8')
        else:
            print('Password too short - require minimum 8 characters!')

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(hashed_password, 'utf-8'))

    def set_new_passwd(self, old_passwd, new_passwd, confirm_new_passwd):
        if User.check_password(old_passwd, self.hashed_password) and new_passwd == confirm_new_passwd:
            self.hashed_password = new_passwd
        else:
            print('Wrong password or new password do not match!')

    def save_to_db(self):
        with psycopg2.connect(COMPLETE_DB_URI) as cnx:
            with cnx.cursor(cursor_factory=RealDictCursor) as curs:
                if self.__id == -1:
                    sql = """INSERT INTO users(username, hashed_password)
                            VALUES (%s, %s) RETURNING id"""
                    values = (self.username, self.hashed_password)
                    curs.execute(sql, values)
                    self.__id = curs.fetchone().get('id')
                    return True
                else:
                    sql = """UPDATE users SET username = %s, hashed_password = %s WHERE id=%s"""
                    values = (self.username, self.hashed_password, self.id)
                    curs.execute(sql, values)
                    return True

    @staticmethod
    def load_user_by_id(user_id):
        with psycopg2.connect(COMPLETE_DB_URI) as cnx:
            with cnx.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """SELECT id, username, hashed_password FROM users WHERE id=%s"""
                curs.execute(sql, (user_id,))
                data = curs.fetchone()
                if data:
                    loaded_user = User()
                    loaded_user.__id = data.get('id')
                    loaded_user.username = data.get('username')
                    loaded_user.__hashed_password = data.get('hashed_password')
                    return loaded_user

    @staticmethod
    def load_user_by_name(username):
        with psycopg2.connect(COMPLETE_DB_URI) as cnx:
            with cnx.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """SELECT id, username, hashed_password FROM users WHERE username=%s"""
                curs.execute(sql, (username,))
                data = curs.fetchone()
                if data:
                    loaded_user = User()
                    loaded_user.__id = data.get('id')
                    loaded_user.username = data.get('username')
                    loaded_user.__hashed_password = data.get('hashed_password')
                    return loaded_user

    @staticmethod
    def load_all_users():
        ret = []
        sql = "SELECT id, username, hashed_password FROM users"
        with psycopg2.connect(COMPLETE_DB_URI) as cnx:
            with cnx.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(sql)
                for row in curs.fetchall():
                    loaded_user = User()
                    loaded_user.__id = row.get('id')
                    loaded_user.username = row.get('username')
                    loaded_user.__hashed_password = row.get('hashed_password')
                    ret.append(loaded_user)
        return ret

    def delete(self):
        with psycopg2.connect(COMPLETE_DB_URI) as cnx:
            with cnx.cursor(cursor_factory=RealDictCursor) as curs:
                sql = "DELETE FROM users WHERE id=%s"
                curs.execute(sql, (self.__id,))
                self.__id = -1
                return True
