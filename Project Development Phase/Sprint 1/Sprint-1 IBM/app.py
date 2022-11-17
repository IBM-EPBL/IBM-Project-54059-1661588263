from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qwq87197;PWD=7TN1X5zgnKSTn9uc",'','')

app = Flask(__name__)



@app.route('/')
def index():
  return render_template("index.html")

@app.route('/login')
def login():
  return render_template("login.html")

@app.route('/signup')
def signup():
  return render_template("signup.html")

@app.route('/regvalidate',methods = ['POST', 'GET'])
def regvalidate():
  if request.method == 'POST':
    username = request.form['username']
    email=request.form['email']
    password = request.form['password']

    
    

    sql = "INSERT INTO Client (username,email,password) VALUES (?,?,?)"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,username)
    ibm_db.bind_param(stmt,2,email)
    ibm_db.bind_param(stmt,3,password)
    
    ibm_db.execute(stmt)

    sql_stmt=ibm_db.exec_immediate(conn,"select * from Client")
    account = ibm_db.fetch_tuple(sql_stmt)

    if account:
      return render_template('validate-success.html')

    else:
      return ("falied")

@app.route('/validate',methods = ['POST', 'GET'])
def validate():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    sql = "SELECT * FROM Client WHERE username =? and password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,username)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('validate-success.html')

    else:
      return ("falied")