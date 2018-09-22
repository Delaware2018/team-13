from flask import (abort, jsonify, g, session, render_template, redirect,
                   request, url_for)
from manage import app
from . import main
import pymongo

@main.route('/')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db
    
    return render_template('index.html')

@main.route('/register')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('register.html')

@main.route('/forgotPassword')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('forgotPassword.html')

@main.route('/about')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('about.html')

@main.route('/FAQ')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('FAQ.html')

@main.route('/home')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('home.html')

@main.route('/resetPassword')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('resetPassword.html')

@main.route('/history')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('history.html')

@main.route('/settings')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('settings.html')

