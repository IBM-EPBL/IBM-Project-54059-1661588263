from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)
app.secret_key = "7847541"

def get_db():
    conn = sqlite3.connect('user_details.db')
    # with open('schema.sql') as schema:
    #     conn.executescript(schema.read())
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/signin', methods=('GET', 'POST'))
def signin():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            'SELECT name FROM user_details WHERE password = ?', (password, )
        ).fetchone()
        
        if user is None:
            error = 'Incorrect Username/Password.'
  

        if error is None:
            return render_template('index.html', title="Home", succ="login successfull!")
        flash(error)
        db.close()

    return render_template('signin.html', title='Sign In', error=error)


@app.route('/signup', methods=('POST', 'GET'))
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        curr = db.cursor()
        
        curr.execute(
            'INSERT INTO user_details (name, email, password) VALUES (?, ?, ? );', (name, email, password )
        )
        db.commit()
        curr.close()
        db.close()
        return render_template('index.html', title="Home", succ="Registration Successfull!")
        

    return render_template('signup.html', title='Sign Up')


