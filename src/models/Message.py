class Message():
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

    @property
    def id(self):
        return self.__id

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text) 
                    VALUES (%s, %s, %s) RETURNING id"""
            values = (self.__from_id, self.__to_id, self.text)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE messages SET text = %s WHERE id=%s"""
            values = (self.text, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = """SELECT id, from_id, to_id, text, creation_date FROM messages WHERE id=%s"""
        cursor.execute(sql, (message_id,))
        data = cursor.fetchone()
        if data:
            loaded_message = Message()
            loaded_message.__id = data['id']
            loaded_message.__from_id = data['from_id']
            loaded_message.__to_id = data['to_id']
            loaded_message.text = data['text']
            loaded_message.creation_date = data['creation_date']
            return loaded_message

    @staticmethod
    def load_all_messages(cursor, user_id=None):
        sql = """SELECT id, from_id, to_id, text, creation_date FROM messages"""
        if user_id:
            sql += " WHERE to_id=%s"
        cursor.execute(sql, (user_id,))
        ret = []
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row['id']
            loaded_message.__from_id = row['from_id']
            loaded_message.__to_id = row['to_id']
            loaded_message.text = row['text']
            loaded_message.creation_date = row['creation_date']
            ret.append(loaded_message)
        return ret

    @staticmethod
    def load_all_messages_for_user(cursor, user_id):
        return Message.load_all_messages(cursor, user_id)
