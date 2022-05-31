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
