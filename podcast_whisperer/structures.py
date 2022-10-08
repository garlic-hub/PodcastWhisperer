from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime


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
    image: str
    last_updated: Optional[int]

    def __init__(self, row: Dict):
        """Init a Show from the results of a database query"""
        self.id = row['id']
        self.name = row['name']
        self.image = row['image']

        # If timestamp is not null, format it into string date
        if row['last_updated']:
            self.last_updated = datetime.fromtimestamp(row['last_updated']).strftime('%b %-d, %Y')
        else:
            self.last_updated = None


@dataclass
class Episode:
    id: int
    name: str

    def __init__(self, row: Dict):
        """Init an Episode from the results of a database query"""
        self.id = row['id']
        self.name = row['name']


def seconds_to_timestamp(seconds: int) -> str:
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return f'{hours:02}:{minutes:02}:{seconds:02}'


@dataclass
class Segment:
    """A segment used when an individual transcript is being used"""
    id: int
    episode: str
    text: str
    timestamp: str

    def __init__(self, row: Dict):
        """Init a Segment from the results of a database query"""
        self.id = row['id']
        self.episode = row['episode']
        self.text = row['text']
        self.timestamp = seconds_to_timestamp(row['timestamp'])


@dataclass
class SearchSegment:
    """A segment used when transcripts are being searched"""
    id: int
    show: str
    episode: str
    text: str
    timestamp: str

    def __init__(self, row: Dict):
        """Init a Segment from the results of a database query"""
        self.id = row['rowid']
        self.show = row['show_name']
        self.episode = row['episode_name']
        self.text = row['text']
        self.timestamp = seconds_to_timestamp(row['timestamp'])
