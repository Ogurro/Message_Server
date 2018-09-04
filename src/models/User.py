import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
from . import COMPLETE_DB_URI
# if __name__ == '__main__':
#     import os
#     COMPLETE_DB_URI = os.environ.get('COMPLETE_DB_URI')


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
        return f"User() # id='{self.id}', username='{self.username}', emil='{self.email}'"

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
                    sql = """INSERT INTO users(username, email, hashed_password)
                            VALUES (%s, %s, %s) RETURNING id"""
                    values = (self.username, self.email, self.hashed_password)
                    curs.execute(sql, values)
                    self.__id = curs.fetchone()['id']
                    return True
                else:
                    sql = """UPDATE users SET username = %s, email = %s, hashed_password = %s WHERE id=%s"""
                    values = (self.username, self.email, self.hashed_password, self.id)
                    curs.execute(sql, values)
                    return True

    #TODO FIX LATER
    #     @staticmethod
    #     def load_user_by_id(cursor, user_id):
    #         sql = """SELECT id, username, email, hashed_password FROM users WHERE id=%s"""
    #         cursor.execute(sql, (user_id,))
    #         data = cursor.fetchone()
    #         if data:
    #             loaded_user = User()
    #             loaded_user.__id = data['id']
    #             loaded_user.username = data['username']
    #             loaded_user.email = data['email']
    #             loaded_user.__hashed_password = data['password_hash']
    #             return loaded_user
    #
    #     @staticmethod
    #     def load_all_users(cursor):
    #         sql = "SELECT id, username, email, hashed_password FROM users"
    #         ret = []
    #         cursor.execute(sql)
    #         for row in cursor.fetchall():
    #             loaded_user = User()
    #             loaded_user.__id = row['id']
    #             loaded_user.username = row['username']
    #             loaded_user.email = row['email']
    #             loaded_user.__hashed_password = row['password_hash']
    #             ret.append(loaded_user)
    #         return ret
    #
    #     def delete(self, cursor):
    #         sql = "DELETE FROM users WHERE id=%s"
    #         cursor.execute(sql, (self.__id,))
    #         self.__id = -1
    #         return True
    #
    # if __name__ == '__main__':
    #     u = User()
    #     u.hashed_password = 'foobarbaz'
    #     print(User.check_password('foobarbaz', u.hashed_password))  # TRUE
    #     print(User.check_password('foobazbar', u.hashed_password))  # FALSE
    #     u.set_new_passwd('foobarbaz', 'foobazbar', 'foobazbar1')  # NEW PASS NOT MACH
    #     u.set_new_passwd('foobarbaz1', 'foobazbar', 'bazfoobar')  # WRONG PASSWD
    #     u.set_new_passwd('foobarbaz', 'foobazbar', 'foobazbar')  # PASSWD changed perform check
    #     print(User.check_password('foobarbaz', u.hashed_password))  # FALSE, old passwd
    print(User.check_password('foobazbar', u.hashed_password))  # TRUE
