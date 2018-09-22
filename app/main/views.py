
from flask import (abort, jsonify, g, session, render_template, redirect,
                   request, url_for)
from functools import wraps
from manage import app
from . import main

import binascii
import hashlib
import uuid
import pymongo

def login_required(f):
    '''
        Allows the passed function to only be executed when the user is
        logged in
    :return:
        decorated function
    '''



    @wraps(f)
    def decorated_function(*args, **kwargs):
        my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

        if(not('user' in session)):
            abort(404)
        # get user db object
        user_exists = my_db.users.find_one({'email':session['user']})

        if(not(user_exists)):
            abort(404)
        # send to whatever page was requested
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('index.html')

@main.route('/register')
def register():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('register.html')

@main.route('/check_user', methods=['POST'])
def check_user():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    data = request.form
    print(data)


    user_exists = my_db.users.find_one({'email': data['email']})

    if(not(user_exists)):
        abort(400)

    hashed_password = hashlib.sha512(data['pass'].encode('utf-8') + user_exists['salt'].encode('utf-8')).hexdigest()


    if(hashed_password != user_exists['password']):
        abort(400)

    session['user'] = data['email']

    return redirect(url_for('.home'))

@main.route('/home')
@login_required
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

    hashed_password = hashlib.sha512(data['pass'].encode('utf-8') + salt.encode('utf-8')).hexdigest()



    my_db.users.insert({
            'fname': data['firstName'],
            'lname': data['lastName'],
            'email': data['email'],
            'pnum': data['pnum'],
            'password': hashed_password,
            'salt': salt,
            'points': 0,
            'rewards': [],
            'donations': []
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

