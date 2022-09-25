from flask import Flask,url_for,render_template,flash,request
import sqlite3 as sql

app = Flask(__name__)


def get_db():
    conn = sql.connect('client_details.db')
    with open('schema.sql') as schema:
       conn.executescript(schema.read())
    #after running it once comment the line to open schema 
    conn.row_factory = sql.Row
    return conn

@app.route("/")
def index():
  return render_template("index.html")



@app.route("/signup", methods=('GET', 'POST'))
def signup():
  if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        curr = db.cursor()
        
        curr.execute(
            'INSERT INTO client_details (username, email, password) VALUES (?, ?, ? );', (name, email, password )
        )
        db.commit()
        curr.close()
        db.close()
        return render_template('welcome.html')
  return render_template("signup.html")



@app.route("/signin", methods=('GET', 'POST'))
def signin():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            'SELECT username FROM client_details WHERE password = ?', (password,)
        ).fetchone()
        
        if user is None:
            error = 'Incorrect Username/Password.'
  

        if error is None:
            return render_template('welcome.html')
        flash(error)
        db.close()
    return render_template("signin.html")


@app.route("/welcome")
def welcome():
  return render_template("welcome.html")


@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)