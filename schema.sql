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

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE movie_classes (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER REFERENCES movies,
    title TEXT,
    value TEXT
);
