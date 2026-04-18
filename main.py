from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_session import Session
import os
import uuid

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = "filesystem"
file_save_location = "static/images"
allowed_types = [".png", ".jpg", ".jpeg"]

Session(app)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/view')
def view():
    return render_template("view.html", movies=session["movies"])

@app.route('/delete', methods=["GET", "POST"])
def delete():
    if request.method == "GET":
        return render_template("delete.html", movies=session["movies"])
    elif request.method == "POST":
        index = int(request.form.get("movieIndex"))
        flash(f"{session["movies"][index].get("movieName")} has been deleted.","message")
        os.remove(session["movies"][index].get("poster"))
        session["movies"].pop(index)
        return redirect("/delete")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        if "movies" not in session:
            print("Getting new session data...")
            session["movies"] = []

        movieName = request.form.get("movieName", "invalid")
        genre = request.form.get("genre", "invalid")
        releaseYear = request.form.get("releaseYear", "invalid")
        rating = request.form.get("rating", "invalid")
        poster = request.files["poster"]

        if poster.filename != "":
            fileext = os.path.splitext(poster.filename)[1]
            if fileext in allowed_types:
                imgUuid = f"{uuid.uuid4().hex}{fileext}"
                filename = os.path.join(file_save_location, imgUuid)
                poster.save(filename)
                session["movies"].append({"movieName": movieName, "genre": genre, "releaseYear": releaseYear, "rating": rating, "poster": filename})
            else:
                flash("Wrong type of file uploaded, try again.", "error")
                return redirect("/add")
            session.modified = True
            print(session.get("movies"))
            return render_template("added.html", movie=movieName)

if __name__ == "__main__":
    app.run(host='0.0.0.0')