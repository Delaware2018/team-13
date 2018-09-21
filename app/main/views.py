from flask import (abort, jsonify, g, session, render_template, redirect,
                   request, url_for)
from manage import app
from . import main
import pymongo

@main.route('/')
def index():
    my_db = pymongo.MongoClient(app.config['MONGO_URL'])
    print(app.config['MONGO_URL'])
    

    print(my_db)
    my_db.admin.users.insert({'test':'test'})
    return render_template('index.html')