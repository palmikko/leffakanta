import secrets
import sqlite3
from flask import Flask
from flask import abort, make_response, redirect, render_template, request, session
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

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
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
    comments = movies.get_comments(movie_id)
    images = movies.get_images(movie_id)
    return render_template("show_movie.html", movie=movie, classes=classes, comments=comments, images=images)

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = movies.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/new_movie")
def new_movie():
    require_login()
    classes = movies.get_all_classes()
    return render_template("new_movie.html", classes=classes)

@app.route("/create_movie", methods=["GET", "POST"])
def create_movie():
    require_login()
    check_csrf()

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

    all_classes = movies.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    movies.add_movie(title, genre, duration, user_id, classes)

    return redirect("/")

@app.route("/create_comment", methods=["GET", "POST"])
def create_comment():
    require_login()
    check_csrf()

    comment = request.form["comment"]
    if not comment or len(comment) > 50:
        abort(403)
    movie_id = request.form["movie_id"]
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(403)
    user_id = session["user_id"]

    movies.add_comment(movie_id, user_id, comment)

    return redirect("/movie/" + str(movie_id))

@app.route("/edit_movie/<int:movie_id>")
def edit_movie(movie_id):
    require_login()
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    all_classes = movies.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in movies.get_classes(movie_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_movie.html", movie=movie, classes=classes,
    all_classes=all_classes)

@app.route("/images/<int:movie_id>")
def edit_images(movie_id):
    require_login()
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    images = movies.get_images(movie_id)

    return render_template("images.html", movie=movie, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    check_csrf()

    movie_id = request.form["movie_id"]
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    file = request.files["image"]
    if not file.filename.endswith(".png"):
        return "VIRHE: väärä tiedostomuoto"

    image = file.read()
    if len(image) > 100 * 1024:
        return "VIRHE: liian suuri kuva"

    movies.add_image(movie_id, image)
    return redirect("/images/" + str(movie_id))

@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    check_csrf()

    movie_id = request.form["movie_id"]
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    for image_id in request.form.getlist("image_id"):
        movies.remove_image(movie_id, image_id)

    return redirect("/images/" + str(movie_id))

@app.route("/update_movie", methods=["POST"])
def update_movie():
    require_login()
    check_csrf()

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

    all_classes = movies.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    movies.update_movie(movie_id, title, genre, duration, classes)

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
        check_csrf()
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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")