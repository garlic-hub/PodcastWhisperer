import io

import pytest


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
    # Output should either have October 12th 2022 or October 13th 2022 depending on timezone
    assert b"Updated: Oct 1" in response.data

    auth.login()
    response = client.get("/")
    check_navbar_logged_in(response)
    # Check that podcast list is there
    assert b"Shakespeare" in response.data
    # Output should either have October 12th 2022 or October 13th 2022 depending on timezone
    assert b"Updated: Oct 1" in response.data


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


@pytest.mark.parametrize(
    ("show", "icon", "message"),
    (
        ("foo", (io.BytesIO(b"abc"), "image.png"), b"Show created"),
        ("foo", (io.BytesIO(b"abc"), "image.PNG"), b"Show created"),
        ("foo", (io.BytesIO(b"abc"), "image.jpg"), b"Show created"),
        ("foo", (io.BytesIO(b"abc"), "image.JPG"), b"Show created"),
        ("foo", (io.BytesIO(b"abc"), "image.jpeg"), b"Show created"),
        ("foo", (io.BytesIO(b"abc"), "image.JPEG"), b"Show created"),
        ("foo", (io.BytesIO(b"abc"), "image.svg"), b"Show created"),
        ("foo", (io.BytesIO(b"abc"), "image.SVG"), b"Show created"),
        (
            "foo",
            (io.BytesIO(b"abc"), "image.h"),
            b"Bad file type. Please use one of the following: png, jpg, jpeg, svg",
        ),
        (
            "foo",
            (io.BytesIO(b"abc"), "image.pdf"),
            b"Bad file type. Please use one of the following: png, jpg, jpeg, svg",
        ),
        (
            "foo",
            (io.BytesIO(b"abc"), "image.py"),
            b"Bad file type. Please use one of the following: png, jpg, jpeg, svg",
        ),
        (
            "foo",
            (io.BytesIO(b"abc"), "image.txt"),
            b"Bad file type. Please use one of the following: png, jpg, jpeg, svg",
        ),
        (
            "foo",
            (io.BytesIO(b"abc"), "image.ico"),
            b"Bad file type. Please use one of the following: png, jpg, jpeg, svg",
        ),
        ("", (io.BytesIO(b"abc"), "image.jpg"), b"Show name cannot be empty"),
        (
            "Shakespeare",
            (io.BytesIO(b"abc"), "image.jpg"),
            b"A show with that name already exists",
        ),
        (
            "Shakespeare",
            (io.BytesIO(b"abc"), "image.jpg"),
            b"A show with that name already exists",
        ),
        ("bar", None, b"Podcast image was not present in request"),
        ("bar", (io.BytesIO(b"abc"), ""), b"Please select a file to upload"),
    ),
)
def test_new_show_post(client, auth, show, icon, message):
    auth.login()
    response = client.post("/new-show", data={"show": show, "image": icon})

    assert message in response.data
    check_navbar_logged_in(response)


@pytest.mark.parametrize(
    ("search", "messages"),
    (
        ("", (b"Search text must be at least 3 characters long",)),
        ("a", (b"Search text must be at least 3 characters long",)),
        ("ab", (b"Search text must be at least 3 characters long",)),
        ("abc", (b"No hits for search query",)),
        ("foo bar", (b"No hits for search query",)),
        ("can't", (b"No hits for search query",)),
        ('can"t', (b"No hits for search query",)),
        # Make sure we don't break on special characters
        ("~!@#$%^&*()_+\\|?/,<.>;:'", (b"No hits for search query",)),
        ("the", (b"Show", b"Episode", b"Timestamp", b"Text")),
        (
            "Stand",
            (b"Shakespeare", b"Hamlet", b"Stand", b"stand", b"00:00:06", b"00:00:01"),
        ),
        (
            "stand",
            (b"Shakespeare", b"Hamlet", b"Stand", b"stand", b"00:00:06", b"00:00:01"),
        ),
        (
            "Who's",
            # The ascii character for apostrophe
            (b"Shakespeare", b"Hamlet", b"Who&#39;s there?", b"00:00:00"),
        ),
    ),
)
def test_search(client, search, messages):
    response = client.get(
        "/search", query_string={"text": search}, follow_redirects=True
    )
    for m in messages:
        assert m in response.data
        check_navbar(response)
