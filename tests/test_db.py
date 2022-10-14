import sqlite3

import pytest
from podcast_whisperer.database import get_db


def test_get_close_db(app):
    # Ensure that get_db() returns the same object each time (per session)
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # Database connection is closed once above with statement is complete
    # Test that db errors out properly
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.con.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('podcast_whisperer.database.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized the database. Note this does not wipe an already created database.\n' == result.output
    assert Recorder.called
