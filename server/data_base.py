import sqlite3

class DataBase:

    def __init__(self):
        self.database = sqlite3.connect('database.db')
        self.cur = self.database.cursor()

        self.cur.execute(''' CREATE TABLE IF NOT EXISTS users
                        (uid INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)''')

        self.database.commit()

    def open_database(self):
        self.database = sqlite3.connect('database.db')
        self.cur = self.database.cursor()

    def add_user(self, username, password):
        self.open_database()
        try:
            self.cur.execute("SELECT * FROM users ORDER BY uid DESC LIMIT 1")
            self.id_personne = self.cur.fetchone()[0] + 1
        except Exception as e:
            self.id_personne = 0

        if self.check_user(username, password) == False:
            self.cur.execute("INSERT INTO users VALUES (?, ?, ?)", (self.id_personne, username, password))
            self.database.commit()
        else:
            return False

    def check_user(self, username, password):
        self.cur.execute("SELECT * FROM users WHERE (username = ? AND password = ?)", (username, password))
        entry = self.cur.fetchone()

        if entry is None:
            return False
        else:
            return True



db = DataBase()

db.add_user("Test", "test")
db.add_user("Toto", "titi")
