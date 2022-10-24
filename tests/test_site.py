import pytest
from podcast_whisperer.database import get_db


def check_navbar(response):
    assert b"Home" in response.data
    assert b"Log In" in response.data
    assert b"Search all transcripts" in response.data


def check_navbar_logged_in(response):
    assert b"Home" in response.data
    assert b"New Show" in response.data
    assert b"Transcribe Episode" in response.data
    assert b"Log Out" in response.data
    assert b"Search all transcripts" in response.data


def test_index(client, auth):
    """Check home page"""
    response = client.get("/")
    check_navbar(response)
    # Check that podcast list is there
    assert b"Shakespeare" in response.data
    assert b"Updated: Oct 12, 2022" in response.data

    auth.login()
    response = client.get("/")
    check_navbar_logged_in(response)
    # Check that podcast list is there
    assert b"Shakespeare" in response.data
    assert b"Updated: Oct 12, 2022" in response.data


@pytest.mark.parametrize(
    "path",
    (
        "/transcribe",
        "/new-show",
    ),
)
def test_login_required(client, path):
    """Check that admin pages can't be accessed without a login"""
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_new_show_get(client, auth):
    """Check that new show page has required form fields"""
    auth.login()
    response = client.get("/new-show")

    assert b"Show Name" in response.data
    assert b"Podcast Icon" in response.data
    assert b"Add Show" in response.data
