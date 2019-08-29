import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from . import COMPLETE_DB_URI


class Message:
    __id = None
    __from_id = None
    __to_id = None
    text = None
    creation_date = None

    def __init__(self):
        self.__id = -1
        self.__from_id = ''
        self.__to_id = ''
        self.text = ''
        self.creation_date = ''

    def __str__(self):
        if self.creation_date:
            date = datetime.strftime(self.creation_date, '%d.%m.%Y %H:%M:%S')
        else:
            date = ''
        return f"""Message | id: {self.id} | from: {self.__from_id} | to: {self.__to_id} | created date: {date}
        text={self.text}
        """

    @property
    def id(self):
        return self.__id

    def save_to_db(self):
        with psycopg2.connect(COMPLETE_DB_URI) as cnx:
            with cnx.cursor(cursor_factory=RealDictCursor) as curs:
                if self.__id == -1:
                    sql = """INSERT INTO messages(from_id, to_id, msg_text) 
                        VALUES (%s, %s, %s) RETURNING id, creation_date"""
                    values = (self.from_id, self.to_id, self.text)
                    curs.execute(sql, values)
                    return_values = curs.fetchone()
                    self.__id = return_values.get('id')
                    self.creation_date = datetime.strftime(return_values.get('creation_date'), '%d.%m.%Y %H:%M:%S')
                    return True
                else:
                    sql = """UPDATE messages SET msg_text = %s WHERE id=%s"""
                    values = (self.text, self.id)
                    curs.execute(sql, values)
                    return True

    @staticmethod
    def load_message_by_id(message_id):
        with psycopg2.connect(COMPLETE_DB_URI) as cnx:
            with cnx.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """SELECT id, from_id, to_id, msg_text, creation_date FROM messages WHERE id=%s"""
                curs.execute(sql, (message_id,))
                data = curs.fetchone()
                if data:
                    loaded_message = Message()
                    loaded_message.__id = data.get('id')
                    loaded_message.__from_id = data.get('from_id')
                    loaded_message.__to_id = data.get('to_id')
                    loaded_message.text = data.get('msg_text')
                    loaded_message.creation_date = data.get('creation_date')
                    return loaded_message

    @staticmethod
    def load_all_messages(to_user_id=None, from_user_id=None):
        with psycopg2.connect(COMPLETE_DB_URI) as cnx:
            with cnx.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """SELECT id, from_id, to_id, msg_text, creation_date FROM messages"""
                ret = []
                if to_user_id:
                    sql += " WHERE to_id=%s"
                    curs.execute(sql, (to_user_id,))
                if from_user_id:
                    sql += " WHERE from_id=%s"
                    curs.execute(sql, (from_user_id,))
                for row in curs.fetchall():
                    loaded_message = Message()
                    loaded_message.__id = row.get('id')
                    loaded_message.__from_id = row.get('from_id')
                    loaded_message.__to_id = row.get('to_id')
                    loaded_message.text = row.get('msg_text')
                    loaded_message.creation_date = row.get('creation_date')
                    ret.append(loaded_message)
                return ret

    @staticmethod
    def load_all_messages_for_user(user_id):
        return Message.load_all_messages(to_user_id=user_id)

    @staticmethod
    def load_all_messages_form_user(user_id):
        return Message.load_all_messages(from_user_id=user_id)

    def delete(self):
        with psycopg2.connect(COMPLETE_DB_URI) as cnx:
            with cnx.cursor(cursor_factory=RealDictCursor) as curs:
                sql = "DELETE FROM messages WHERE id=%s"
                curs.execute(sql, (self.__id,))
                self.__id = -1
                return True


if __name__ == '__main__':
    m = Message.load_message_by_id(19)
    print(m)
