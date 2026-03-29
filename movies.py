import db

def add_movie(title, genre, duration, user_id):
        sql = """INSERT INTO movies (title, genre, duration, user_id)
                 VALUES (?, ?, ?, ?)"""
        db.execute(sql, [title, genre, duration, user_id])