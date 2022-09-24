import sqlite3


class Database:
    def __init__(self, file='whisperer.db'):
        self.con = sqlite3.connect(file)
        self.init_db()

    def init_db(self):
        self.con.executescript('init.sql')
