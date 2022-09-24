-- Where the names of a show are stored
CREATE TABLE IF NOT EXISTS "shows" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE COLLATE NOCASE,
    PRIMARY KEY("id")
);

-- Where the transcripts and timestamps for an episode are stored
CREATE TABLE IF NOT EXISTS "episodes" (
    "id" INTEGER,
    "show" INTEGER NOT NULL,
    "text" TEXT NOT NULL,
    "timestamps" TEXT NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("show") REFERENCES "shows"("id")
);

-- The index for full text search on transcripts
CREATE VIRTUAL TABLE IF NOT EXISTS "text_index" USING fts5 (
    text,
    content=episodes,
    content_rowid=id,
    tokenize="trigram"
);

-- Triggers to keep the FTS index up to date
CREATE TRIGGER IF NOT EXISTS episodes_ai AFTER INSERT ON episodes BEGIN
  INSERT INTO text_index(rowid, text) VALUES (new.rowid, new.text);
END;
CREATE TRIGGER IF NOT EXISTS episodes_ad AFTER DELETE ON episodes BEGIN
  INSERT INTO text_index(text_index, rowid, text) VALUES('delete', old.rowid, old.text);
END;
CREATE TRIGGER IF NOT EXISTS episodes_au AFTER UPDATE ON episodes BEGIN
  INSERT INTO text_index(text_index, rowid, text) VALUES('delete', old.rowid, old.text);
  INSERT INTO text_index(rowid, text) VALUES (new.rowid, new.text);
END;
