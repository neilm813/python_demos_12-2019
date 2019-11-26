from flask import Flask, render_template, redirect, request, session
import os
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/guest/<name>')
def guest(name):
    uid = uuid.uuid4().hex
    return render_template("guest.html", guest_name=name, id=uid)


@app.route('/users/<uid>')
def user_profile(uid):
    return render_template("user_profile.html", id=uid)


@app.route('/<path:path>')
def unkown_route(path):
    return f"unknown path: {path}"


if __name__ == "__main__":
    app.run(debug=True)
