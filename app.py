import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import movies
import re
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_movies = movies.get_movies()
    return render_template("index.html", movies=all_movies)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    movies = users.get_movies(user_id)
    return render_template("show_user.html", user=user, movies=movies)

@app.route("/find_movie")
def find_movie():
    query = request.args.get("query")
    if query:
        results = movies.find_movies(query)
    else:
        query = ""
        results = []
    return render_template("find_movie.html", query=query, results=results)

@app.route("/movie/<int:movie_id>")
def show_movie(movie_id):
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    classes = movies.get_classes(movie_id)
    return render_template("show_movie.html", movie=movie, classes=classes)

@app.route("/new_movie")
def new_movie():
    require_login()
    classes = movies.get_all_classes()
    return render_template("new_movie.html", classes=classes)

@app.route("/create_movie", methods=["GET", "POST"])
def create_movie():
    require_login()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    genre = request.form["genre"]
    if not genre or len(genre) > 50:
        abort(403)
    duration = request.form["duration"]
    if not re.search("^[1-9][0-9]{0,3}$", duration):
        abort(403)
    user_id = session["user_id"]

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0], parts[1]))

    movies.add_movie(title, genre, duration, user_id, classes)

    return redirect("/")

@app.route("/edit_movie/<int:movie_id>")
def edit_movie(movie_id):
    require_login()
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_movie.html", movie = movie)

@app.route("/update_movie", methods=["POST"])
def update_movie():
    require_login()
    movie_id = request.form["movie_id"]
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    genre = request.form["genre"]
    if not genre or len(genre) > 50:
        abort(403)
    duration = request.form["duration"]
    if not re.search("^[1-9][0-9]{0,3}$", duration):
        abort(403)

    movies.update_movie(movie_id, title, genre, duration)

    return redirect("/movie/" + str(movie_id))

@app.route("/remove_movie/<int:movie_id>", methods=["GET", "POST"])
def remove_movie(movie_id):
    require_login()
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_movie.html", movie = movie)

    if request.method == "POST":
        if "remove" in request.form:
            movies.remove_movie(movie_id)
            return redirect("/")
        else:
            return redirect("/movie/" + str(movie_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"



@app.route("/login", methods=["GET" ,"POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/login")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/login")