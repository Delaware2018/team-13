from flask import (abort, jsonify, g, session, render_template, redirect,
                   request, url_for)
from manage import app#, client
from . import main
# import self written modules from modules dir
# from ..modules import ...

@main.route('/')
def index():
    return render_template('index.html')