import sqlite3

class DataBase:

    def __init__(self):
        self.database = sqlite3.connect('database.db')
        self.cur = self.database.cursor()

        self.cur.execute(''' CREATE TABLE IF NOT EXISTS users
                        (uid INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)''')

        self.cur.execute(''' CREATE TABLE IF NOT EXISTS admins
                        (admin_id INTEGER PRIMARY KEY AUTOINCREMENT, uid integer)''')

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

        if self.check_username(username) == False:
            self.cur.execute("INSERT INTO users VALUES (?, ?, ?)", (self.id_personne, username, password))
            self.database.commit()
            return True
        else:
            return False

    def check_user(self, username, password):
        self.open_database()
        self.cur.execute("SELECT * FROM users WHERE (username = ? AND password = ?)", (username, password))
        entry = self.cur.fetchone()

        if entry is None:
            return False
        else:
            return True

    def check_username(self, username):
        self.open_database()
        self.cur.execute("SELECT * FROM users WHERE (username = ?)", (username,))
        entry = self.cur.fetchone()

        if entry is None:
            return False
        else:
            return True


    def add_admin(self, uid):
        self.open_database()
        try:
            self.cur.execute("SELECT * FROM admins ORDER BY admin_id DESC LIMIT 1")
            self.id_personne = self.cur.fetchone()[0] + 1
        except Exception as e:
            self.id_personne = 0

        self.cur.execute("SELECT * FROM users WHERE (uid  = ?)", (uid,))
        entry = self.cur.fetchone()

        self.cur.execute("SELECT * FROM admins WHERE (uid = ?)", (uid,))
        entry2 = self.cur.fetchone()

        if entry is None:
            return False
        else:
            if entry2 is None:
                self.cur.execute("INSERT INTO admins VALUES (?, ?)", (self.id_personne, uid))
                self.database.commit()
                return True
            else:
                return False


    def check_if_user_is_admin(self, username):

        self.cur.execute("SELECT * FROM users WHERE (username  = ?)", (username,))
        entry = self.cur.fetchone()

        self.cur.execute("SELECT * FROM admins WHERE (uid = ?)", (entry[0],))
        entry2 = self.cur.fetchone()

        if entry2 is None:
            return False
        else:
            return True



db = DataBase()
