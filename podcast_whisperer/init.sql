-- Where admins accounts are stored
CREATE TABLE IF NOT EXISTS "users" (
  "id" INTEGER,
  "username" TEXT UNIQUE NOT NULL,
  "password" TEXT NOT NULL,
  PRIMARY KEY("id")
);

-- Where the names of a show are stored
-- image is a relative path to the image
CREATE TABLE IF NOT EXISTS "shows" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE COLLATE NOCASE,
    "image" TEXT NOT NULL,
    "last_updated" INTEGER,
    PRIMARY KEY("id")
);

-- Where the transcripts and timestamps for an episode are stored
CREATE TABLE IF NOT EXISTS "episodes" (
    "id" INTEGER,
    "show" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("show") REFERENCES "shows"("id")
);

CREATE TABLE IF NOT EXISTS "segments" (
    "id" INTEGER,
    "episode" INTEGER,
    "text" TEXT NOT NULL,
    "timestamp" INTEGER NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("episode") REFERENCES "episodes" ("id")
);

-- The index for full text search on transcripts
CREATE VIRTUAL TABLE IF NOT EXISTS "text_index" USING fts5 (
    text,
    content=segments,
    content_rowid=id,
);

-- Triggers to keep the FTS index up to date
CREATE TRIGGER IF NOT EXISTS segments_ai AFTER INSERT ON segments BEGIN
  INSERT INTO text_index(rowid, text) VALUES (new.rowid, new.text);
END;
CREATE TRIGGER IF NOT EXISTS segments_ad AFTER DELETE ON segments BEGIN
  INSERT INTO text_index(text_index, rowid, text) VALUES('delete', old.rowid, old.text);
END;
CREATE TRIGGER IF NOT EXISTS segments_au AFTER UPDATE ON segments BEGIN
  INSERT INTO text_index(text_index, rowid, text) VALUES('delete', old.rowid, old.text);
  INSERT INTO text_index(rowid, text) VALUES (new.rowid, new.text);
END;
