import pytest
from flask import g, session

from podcast_whisperer.auth import create_admin


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user.username == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", b"Bad login"),
        ("test", "a", b"Bad login"),
        ("", "a", b"Bad login"),
        ("a", "", b"Bad login"),
        ("", "", b"Bad login"),
    ),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


@pytest.mark.parametrize(
    ("username", "password", "exit_code", "message"),
    (
        ("admin", "admin", 0, "New admin created\n"),
        ("", "", 1, "Username cannot be empty\n"),
        ("", "password", 1, "Username cannot be empty\n"),
        ("username", "", 1, "Password cannot be empty\n"),
    ),
)
def test_create_admin(runner, username, password, exit_code, message):
    result = runner.invoke(create_admin, [username, password])
    assert result.exit_code == exit_code
    assert result.output == message


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
