import db

def add_movie(title, genre, duration, user_id):
        sql = """INSERT INTO movies (title, genre, duration, user_id)
                 VALUES (?, ?, ?, ?)"""
        db.execute(sql, [title, genre, duration, user_id])

def get_movies():
    sql = "SELECT id, title FROM movies ORDER BY id DESC"
    return db.query(sql)

def get_movie(movie_id):
    sql = """SELECT movies.title,
                    movies.genre,
                    movies.duration,
                    users.username
             FROM movies, users
             WHERE movies.user_id = users.id AND
                   movies.id = ?"""
    return db.query(sql, [movie_id])[0]