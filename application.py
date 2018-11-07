from flask import Flask, render_template, request, session
#import mysql.connector
import hashlib

import os

import pymysql.cursors
from bcrypt import hashpw, gensalt

# Connect to the database.
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='spshare',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

if connection.open:
    print("connection successful bro LMAO..")
else:
    print("failed")
cursor = connection.cursor()

application = Flask(__name__)
application.secret_key = os.urandom(24)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    #return render_template('homepage.html')
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        #print(username)
        #print(password)

        hashed = hashpw(password.encode('utf8'), gensalt())
        #print(hashed)
        query = "select count(*) from users where username = '" + str(username) + "' and password = '" + hashed + "'"
        cursor.execute(query)
        #print(cursor._last_executed)
        data = cursor.fetchall()
        print(data)
        if data:
            session['user'] = username
            print (session['user'])
            return render_template('homepage.html')
        else:
            return render_template('index.html')

@application.route('/register', methods=['GET', 'POST'])
def register1():
    if request.method=='POST':
        return render_template('register.html')

@application.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    if request.method=='POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        hashed = hashpw(password.encode('utf8'), gensalt())
        query = "select into users(name, username, password) values(%s, %s, %s)"
        cursor.execute(query, (str(name), str(username), hashed))



if __name__ == '__main__':
    application.run()