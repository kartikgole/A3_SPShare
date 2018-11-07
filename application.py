import binascii

from flask import Flask, render_template, request, session
#import mysql.connector
import hashlib

import os

import pymysql.cursors
from bcrypt import hashpw, gensalt
import ctypes  # An included library with Python install.

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

    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']


        encpass = password.encode('ASCII')
        dk = hashlib.pbkdf2_hmac('SHA256', encpass, b'salt', 100000).strip()
        print(dk)
        newhashed = str(binascii.hexlify(dk))

        finalhashed = newhashed[1:]
        print(finalhashed)
        query = "select * from users where username = '" + str(username) + "' and password =  " + finalhashed +" "
        print(query)
        cursor.execute(query)

        data = cursor.fetchall()
        print(data)
        if data:
            session['user'] = username
            print (session['user'])
            return render_template('SPShareHome.html')
        else:
            return render_template('LoginFailed.html')

@application.route('/register', methods=['GET', 'POST'])
def register1():
    if request.method=='POST':
        return render_template('register.html')

@application.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    if request.method=='POST':
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db='spshare',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        encpass = password.encode('ASCII')
        dk = hashlib.pbkdf2_hmac('SHA256', encpass, b'salt', 100000).strip()
        print(dk)
        newhashed = binascii.hexlify(dk)
        print(newhashed)
        query = "insert into users(name, username, password) values(%s, %s, %s)"
        print(query, (name, username, newhashed))
        cursor.execute(query, (name, username, newhashed))
        connection.commit()
        ctypes.windll.user32.MessageBoxW(0, "Success", "You have been registered, now Log in", 1)
        return render_template('index.html')


if __name__ == '__main__':
    application.run()