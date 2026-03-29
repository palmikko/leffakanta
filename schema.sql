CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE,
    genre TEXT,
    duration INTEGER,
    user_id INTEGER REFERENCES users
);