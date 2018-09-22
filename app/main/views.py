
from flask import (abort, jsonify, g, session, render_template, redirect,
                   request, url_for)
from manage import app
from . import main

import binascii
import hashlib
import uuid
import pymongo

@main.route('/')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db
    
    return render_template('index.html')

@main.route('/register')
def register():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('register.html')

@main.route('/check_user', methods=['GET'])
def check_user():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    data = request.form


    user_exists = my_db.users.find_one({'email': data['email']})

    if(not(user_exists)):
        abort(400)

    hashed_password = hashlib.sha512(data['pass'].encode('utf-8') + user_exists['salt'].encode('utf-8')).hexdigest()

    if(not(hashed_password is user_exists['password'])):
        abort(400)

    return redirect(url_for('.home'))



@main.route('/home')
def home():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db
    
    return render_template('home.html')

@main.route('/add_user', methods=['POST'])
def add_user():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    data = request.form


    user_exists = my_db.users.find_one({'$or': [
            {'email': data['email']},
            {'pnum': data['pnum']}
        ]})



    if(user_exists):
        abort(400)

    if(data['pass'] != data['confirm_pass']):
        abort(405)

    salt = uuid.uuid4().hex
    print(salt)

    hashed_password = hashlib.sha512(data['pass'].encode('utf-8') + salt.encode('utf-8')).hexdigest()



    my_db.users.insert({
            'fname': data['firstName'],
            'lname': data['lastName'],
            'email': data['email'],
            'pnum': data['pnum'],
            'password': hashed_password,
            'salt': salt
        })

    return jsonify({'status': 'complete'})


@main.route('/forgot_password')
def forgotPass():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('forgot_password.html')

@main.route('/about')
def about():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('about.html')

@main.route('/FAQ')
def faq():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('FAQ.html')

@main.route('/resetPassword')
def resetPass():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('resetPassword.html')

@main.route('/history')
def history():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('history.html')

@main.route('/settings')
def settings():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('settings.html')

