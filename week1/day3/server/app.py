from flask import Flask, render_template, redirect, request, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

users = []


@app.route('/')
def home():
    return render_template('index.html', all_users=users)


@app.route('/register', methods=['POST'])
def register():

    new_user = {
        'name': request.form['name'],
        'age': request.form['age'],
        'favorite-quote': request.form['favorite-quote']
    }

    users.append(new_user)

    return redirect('/')


@app.route('/users/<idx_str>')
def user_profile(idx_str):

    idx = int(idx_str)
    user = users[idx]

    return render_template('user_profile.html', selected_user=user)


if __name__ == "__main__":
    app.run(debug=True)
