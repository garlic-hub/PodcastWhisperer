import sqlite3
from typing import List, Tuple


class Database:
    def __init__(self, file='whisperer.db'):
        self.con = sqlite3.connect(file)
        self.init_db()

    def init_db(self):
        with open('init.sql', 'r') as script:
            self.con.executescript(script.read())

    def create_show(self, name=str):
        self.con.execute('INSERT INTO shows(name) VALUES (:show)', (name,))
        self.con.commit()

    def get_shows(self) -> List[Tuple[str, str]]:
        shows = self.con.execute('SELECT * FROM shows')
        return shows.fetchall()
