import sqlite3

class BotDB:

    def __init__(self, user_db):
        """Инициализируем соеденение с БД"""
        self.conn = sqlite3.connect(user_db)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем уникальность юзера в БД"""
        result = self.cursor.execute("SELECT 'user_id' FROM 'users' WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))
    
    def get_user_id(self, user_id):
        """Получаем id юзера в БД по его user_id в телеграме"""
        result = self.cursor.execute("SELECT 'id' FROM 'user' WHERE 'user_id' = ?", (user_id))
        return result.fetchone()[0]

    def add_user(self, user_id, first_name):
        """Добавляем юзера в БД"""
        self.cursor.execute("INSERT INTO 'users' ('user_id', 'F_I_O') VALUES(?, ?)", (user_id, first_name,))
        return self.conn.commit()

    def add_data_users(self, user_id, addres, number, comment, fio):
        """Создаем запись данных юзера"""
        self.cursor.execute("INSERT INTO 'Data_users' ('user_id', 'addres', 'number', 'comment', 'fio') VALUES(?, ?, ?, ?, ?)",
            (user_id,
            addres,
            number,
            comment,
            fio))
        return self.conn.commit()

    def number_of_users(self):
        result = self.cursor.execute("SELECT user_id FROM 'users'")
        return result.fetchall()

    def info_of_participants(self):
        result = self.cursor.execute("SELECT * FROM 'Data_users'")
        return result.fetchall()

    def close(self):
        """Закрытие БД"""
        self.conn.close()