-- Username and password of test test
INSERT INTO users(id, username, password) VALUES
    (1, 'test', 'pbkdf2:sha256:260000$T0oxraPKYivDzoVB$4418864d6d19581ab6a5dc056399aef0b9342c0d4343b241aa7868d3c76345e9');

INSERT INTO shows(id, name, image, last_updated) VALUES
    (1, 'Shakespeare', 'shakespeare.jpg', '1665631800.34804');

-- Hamlet text is public domain and was obtained via opensourceshakespeare.org
INSERT INTO episodes(id, show, name) VALUES
    (1, 1, 'Hamlet');

INSERT INTO segments(id, episode, text, timestamp) VALUES
    (1, 1, 'Who''s there?', 0),
    (2, 1, 'Nay, answer me. Stand and unfold yourself.', 1),
    (3, 1, 'Long live the King!', 2),
    (4, 1, 'Bernardo?', 3),
    (5, 1, 'He.', 4),
    (6, 1, 'You come most carefully upon your hour', 5);