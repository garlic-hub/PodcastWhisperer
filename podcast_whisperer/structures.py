from dataclasses import dataclass
from typing import Dict


@dataclass
class User:
    """Structure to maintain data pertaining to a logged-in user"""
    id: int
    username: str
    hashed_password: str

    def __init__(self, row: Dict):
        """Init a User from the results of a database query"""
        self.id = row['id']
        self.username = row['username']
        self.hashed_password = row['password']


@dataclass
class Show:
    id: int
    name: str

    def __init__(self, row: Dict):
        """Init a Show from the results of a database query"""
        self.id = row['id']
        self.name = row['name']


@dataclass
class Segment:
    id: int
    show: str
    episode: str
    text: str
    timestamp: str

    def __init__(self, row: Dict):
        """Init a Segment from the results of a database query"""
        print(row)
        self.id = row['rowid']
        self.show = row['show_name']
        self.episode = row['episode_name']
        self.text = row['text']
        self.timestamp = row['timestamps']
