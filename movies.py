import db

def add_movie(title, genre, duration, user_id):
        sql = """INSERT INTO movies (title, genre, duration, user_id)
                 VALUES (?, ?, ?, ?)"""
        db.execute(sql, [title, genre, duration, user_id])

def get_movies():
    sql = "SELECT id, title FROM movies ORDER BY id DESC"
    return db.query(sql)

def get_movie(movie_id):
    sql = """SELECT movies.id,
                    movies.title,
                    movies.genre,
                    movies.duration,
                    users.id user_id,
                    users.username
             FROM movies, users
             WHERE movies.user_id = users.id AND
                   movies.id = ?"""
    return db.query(sql, [movie_id])[0]

def update_movie(movie_id, title, genre, duration):
    sql = """UPDATE movies SET title = ?,
                               genre = ?,
                               duration = ?
                           Where id = ?"""
    db.execute(sql, [title, genre, duration, movie_id])

def remove_movie(movie_id):
    sql = "DELETE FROM movies Where id = ?"
    db.execute(sql, [movie_id])