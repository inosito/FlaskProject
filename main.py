from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = "filesystem"

Session(app)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/view')
def view():
    return render_template("view.html")

@app.route('/edit')
def edit():
    return render_template("edit.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')