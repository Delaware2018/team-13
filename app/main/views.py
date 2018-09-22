
from flask import (abort, jsonify, g, session, render_template, redirect,
                   request, url_for)
from manage import app
from . import main

import binascii
import hashlib
import uuid
import time
import pymongo

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


    print(data['email'])
    user_exists = my_db.users.find_one({'email': data['email']})

    if(not(user_exists)):
        abort(400)

    hashed_password = hashlib.sha512(data['pass'].encode('utf-8') + user_exists['salt'].encode('utf-8')).hexdigest()

    print(hashed_password)
    print(user_exists['password'])

    if(hashed_password != user_exists['password']):
        abort(400)

    if(len(user_exists['email']) > 11 and user_exists['email'][-12:] == "goodwill.org"):
        redirect(url_for('.admin'))

    return redirect(url_for('.home'))

@main.route('/add_points', methods=['POST'])
def add_points():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    data = request.form
    print(data)


    print(data['pnum'])
    user_exists = my_db.users.find_one({'pnum': data['pnum']})

    if(not(user_exists)):
        abort(400)

    if(data['poll'] == False):
        id = str(uuid.uuid4())[:4]
        user_exists['donations'].append({'timestamp': time.time(), 'id': id, 
            'pollAnswers': {'what': {'clothes': False, 'furniture': False, 'books': False, 'electronics': False, 'other': False}, 'value': 0}})

    new_points = 0
    if(user_exists['points'] + 10 >= 100):
        new_points = 0
        code = str(uuid.uuid4())[:4]
        while(my_db.incentives.find_one({'code': code})):
            code = str(uuid.uuid4())[:4]
        my_db.incentives.insert({'timestamp': time.time(), 'code': code, 'pnum': data['pnum'], 'desc': ""})
        user_exists['incentives'].append(my_db.incentives.find_one({'pnum': data['pnum']}))
    else:
        new_points = user_exists['points']+10

    my_db.users.updateOne(
      { "pnum" : data["pnum"] },
      { set: { "points" : new_points } })

    return 

@main.route('/admin')
def admin():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db
    
    return render_template('admin.html')	
	
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

