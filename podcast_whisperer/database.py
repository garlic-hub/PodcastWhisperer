import sqlite3

import click
from flask import current_app, g
from typing import List, Tuple, Iterable, Optional

from .structures import User, Show, Segment, SearchSegment, Episode


def get_db():
    if 'db' not in g:
        g.db = Database(current_app.config['DATABASE'])

    return g.db


def init_db():
    get_db().init_db()


@click.command('init-db')
def init_db_command():
    """Initialize the database if it is empty"""
    init_db()
    click.echo('Initialized the database. Note this does not wipe an already created database.')


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


class Database:
    def __init__(self, file):
        self.con = sqlite3.connect(file, detect_types=sqlite3.PARSE_DECLTYPES)
        self.con.row_factory = sqlite3.Row

    def init_db(self):
        with current_app.open_resource('init.sql') as script:
            self.con.executescript(script.read().decode('utf8'))

    def close(self):
        self.con.close()

    def create_user(self, username=str, hashed_password=str):
        self.con.execute('INSERT INTO users(username, password) VALUES (:user, :pass)', (username, hashed_password))
        self.con.commit()

    def get_user_by_id(self, id: int) -> Optional[User]:
        result = self.con.execute('SELECT * FROM users WHERE id = :id', (id,)).fetchone()
        if result:
            return User(result)
        else:
            return None

    def get_user_by_name(self, username: str) -> Optional[User]:
        result = self.con.execute('SELECT * FROM users WHERE username = :user', (username,)).fetchone()
        if result:
            return User(result)
        else:
            return None

    def create_show(self, name=str):
        self.con.execute('INSERT INTO shows(name) VALUES (:user)', (name,))
        self.con.commit()

    def get_shows(self) -> List[Show]:
        cursor = self.con.execute('SELECT * FROM shows')
        return [Show(s) for s in cursor.fetchall()]

    def get_show_by_name(self, name: str):
        result = self.con.execute('SELECT * FROM shows WHERE name = :name', (name,)).fetchone()
        if result:
            return Show(result)
        else:
            return None

    def get_episodes(self, show: int) -> List[Episode]:
        cursor = self.con.execute('SELECT * FROM episodes WHERE show = :show ', (show,))
        return [Episode(e) for e in cursor.fetchall()]

    def add_transcription(self, show: int, name: str, transcription: Iterable[str], timestamps: Iterable[str]):
        cursor = self.con.execute('INSERT INTO episodes(show, name) VALUES (:show, :name)', (show, name))
        rows = ((cursor.lastrowid, x, y) for x, y in zip(transcription, timestamps, strict=True))
        self.con.executemany('INSERT INTO segments(episode, text, timestamp) VALUES (:ep, :text, :stamp)', rows)
        self.con.commit()

    def get_transcript(self, episode_id: int) -> List[Segment]:
        cursor = self.con.execute('SELECT * FROM segments WHERE episode = :epsiode_id', (episode_id,))
        return [Segment(s) for s in cursor.fetchall()]

    def search_transcripts(self, text: str) -> List[SearchSegment]:
        cursor = self.con.execute('''SELECT rowid, text, timestamp, episodes.name AS episode_name, shows.name AS show_name FROM segments
            JOIN (SELECT rowid FROM text_index(:text) ORDER BY rank LIMIT 25) ON segments.id = rowid 
            JOIN episodes ON segments.episode = episodes.id
            JOIN shows ON episodes.show = shows.id;''', (text,))

        return [SearchSegment(s) for s in cursor.fetchall()]
