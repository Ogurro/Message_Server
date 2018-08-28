import clcrypto
from psycopg2 import connect
from psycopg2.extras import DictCursor



class User:
    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = -1
        self.username = ''
        self.email = ''
        self.__hashed_password = ''

    def __str__(self):
        return 'username:%s\nemail:%s\nid:%s' % (self.username, self.email, self.id)

    @property
    def id(self):
        return self.__id

    @property
    def password_hash(self):
        return self.__hashed_password

    @password_hash.setter
    def password_hash(self, password, salt=None):
        self.__hashed_password = clcrypto.password_hash(password, salt)

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statments
            sql = """INSERT INTO users(username, email, password_hash) 
                    VALUES (%s, %s, %s) RETURNING id"""
            values = (self.username, self.email, self.password_hash)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE users SET username = %s, email = %s, password_hash = %s WHERE id=%s"""
            values = (self.username, self.email, self.password_hash, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = """SELECT id, username, email, password_hash FROM users WHERE id=%s"""
        cursor.execute(sql, (user_id,))
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data['id']
            loaded_user.username = data['username']
            loaded_user.email = data['email']
            loaded_user.__hashed_password = data['password_hash']
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, email, password_hash FROM users"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = row['id']
            loaded_user.username = row['username']
            loaded_user.email = row['email']
            loaded_user.__hashed_password = row['password_hash']
            ret.append(loaded_user)
        return ret

    def delete(self, cursor):
        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (self.__id, ))
        self.__id = -1
        return True
