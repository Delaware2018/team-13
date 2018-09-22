
import datetime
from flask import (abort, jsonify, g, session, render_template, redirect,
                   request, url_for)
from functools import wraps
from manage import app, moment
from . import main

import binascii
import hashlib
import uuid
import pymongo
import random

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

@main.route('/logout')
@login_required
def logout():


    return redirect(url_for('.index'))

@main.route('/register')
def register():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    return render_template('register.html')

@main.route('/check_user', methods=['POST'])
def check_user():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    data = request.form

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
    def merge_sort_time(job_list):
        if len(job_list) > 1:
            mid = len(job_list) // 2
            lefthalf = job_list[:mid]
            righthalf = job_list[mid:]

            merge_sort_time(lefthalf)
            merge_sort_time(righthalf)

            i = 0
            j = 0
            k = 0
            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i]['timestamp'] > righthalf[j]['timestamp']:
                    job_list[k] = lefthalf[i]
                    i = i + 1
                else:
                    job_list[k] = righthalf[j]
                    j = j + 1
                k = k + 1

            while i < len(lefthalf):
                job_list[k] = lefthalf[i]
                i = i + 1
                k = k + 1

            while j < len(righthalf):
                job_list[k] = righthalf[j]
                j = j + 1
                k = k + 1

    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db
    

    user = my_db.users.find_one({'email': session['user']})

    if(not(user)):
        abort(404)

    user['donations'].extend(user['rewards'])

    merge_sort_time(user['donations'])

    formatted_events = []
    for event in user['donations']:
        # if it's a reward
        if('code' in event.keys()):
            formatted_event = '''
                <div class="incentive">
                    <span class="incentive-trophy">
                        <i class="fa fa-trophy" aria-hidden="true"></i>
                        <span class="mt">-100</span>
                    </span>
                    <span class="donation-desc">
                       {desc}
                       <b>Code: {code}</b>
                    </span>
                </div>
                '''.format(desc=event['desc'], code=event['code'])
        else:
            c1, c2, c3, c4, c5 = ('','','','','')
            if(event['pollAnswers']['what']['clothes']):
                c1 = 'checked'
            if(event['pollAnswers']['what']['furniture']):
                c2 = 'checked'
            if(event['pollAnswers']['what']['books']):
                c3 = 'checked'
            if(event['pollAnswers']['what']['electronics']):
                c4 = 'checked'
            if(event['pollAnswers']['what']['other']):
                c5 = 'checked'
            formatted_event = '''
                <div class="donation">
                    <span class="donation-check">
                        <i class="fa fa-check-circle-o" aria-hidden="true"></i>
                        <span class="mt">+10</span>
                    </span>
                    <span class="donation-desc">
                        <b>Donation at:</b> {timestamp}
                    </span>
                    <i class="fa fa-chevron-down donation-interact"   aria-hidden="true"></i>
                    <div class="donation-interactions">
                        <div class="col-md-5 sub-pane">
                            <h5>What did you donate?</h5>
                            <form id="donate-what"
                                  style="text-align: left">
                                <input type="checkbox" value="clothes" {c1} />
                                Clothes <br>
                                <input type="checkbox" value="furniture" {c2} />
                                Furniture <br>
                                <input type="checkbox" value="books" {c3} />
                                Books <br>
                                <input type="checkbox" value="electronics" {c4} />
                                Electronics <br>
                                <input type="checkbox" value="other" {c5} />
                                Other <br>
                                <br>
                                <input type="hidden" value="{i_id}">
                                <button class="btn btn-success">
                                    Submit
                                </button>
                            </form>
                        </div>
                        <div class="col-md-5 sub-pane"
                             style="text-align: left">
                            
                            <form id="estimate-val" style="display: inline-block;">
                                <h5 style="display: inline-block">
                                    Estimated Value:
                                </h5>
                                <input type="text" placeholder="$$.$$"
                                       required="" value="{value}"
                                       style="width: 50px; display: inline-block;" />
                                <input type="hidden" value="{i_id}" />

                                <button class="btn btn-success">
                                    Submit
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
                '''.format(timestamp=moment.create(event['timestamp']).format('h:mm a, MMMM Do YYYY'), i_id=event['id'], c1=c1, c2=c2,
                    c3=c3, c4=c4, c5=c5, value=event['pollAnswers']['value'])
        formatted_events.append(formatted_event)
    formatted_events = ''.join(formatted_events)


    return render_template('home.html', score=user['score'],
                           formatted_events=formatted_events)

@main.route('/value_form', methods=['POST'])
@login_required
def value_form():
    reward_pool = ['15% off next purchase', '$5 gift card',
                   '10% next purchase']

    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    data = request.form
    print(data)
    user = my_db.users.find_one({'email': session['user']})

    if(not(user)):
        abort(404)

    new_score = user['score']
    for donation in user['donations']:

        if(donation['id'] == data['donation_id']):
            prev_touched = not(donation['pollAnswers']['value'])
            donation['pollAnswers']['value'] = data['value']

            if(prev_touched):
                new_score += 10

            if(new_score >= 100):
                new_reward = {
                    'timestamp': datetime.datetime.now(),
                    'code': str(uuid.uuid4())[:4],
                    'desc': random.choice(reward_pool),
                    'pnum': user['pnum'],
                    'id': str(uuid.uuid4())
                }

                my_db.rewards.insert(new_reward)
                user['rewards'].append(new_reward)
                new_score = 0


    my_db.users.update({'email': session['user']},
                       {
                        '$set': {
                            'score': new_score,
                            'donations': user['donations'],
                            'rewards': user['rewards']
                        }
                       })
    return jsonify({'status': 'updated'})



@main.route('/what_form', methods=['POST'])
@login_required
def set_what_form():
    reward_pool = ['15% off next purchase', '$5 gift card',
                   '10% next purchase']

    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    data = request.form

    user = my_db.users.find_one({'email': session['user']})

    if(not(user)):
        abort(404)

    new_score = user['score']
    for donation in user['donations']:
        print((donation['id'], data['donation_id']))
        if(donation['id'] == data['donation_id']):
            prev_touched = (not('touched' in donation['pollAnswers']['what']) 
                            or not(donation['pollAnswers']['what']['touched']))
            donation['pollAnswers']['what'] = {
                    'clothes': data['clothes']=='true',
                    'furniture': data['furniture']=='true',
                    'books': data['books']=='true',
                    'electronics': data['electronics']=='true',
                    'other': data['other']=='true',
                    'touched': True
                }
            new_score = user['score']
            if(prev_touched):
                new_score += 10

            if(new_score >= 100):
                new_reward = {
                    'timestamp': datetime.datetime.now(),
                    'code': str(uuid.uuid4())[:4],
                    'desc': random.choice(reward_pool),
                    'pnum': user['pnum'],
                    'id': str(uuid.uuid4())
                }

                my_db.rewards.insert(new_reward)
                user['rewards'].append(new_reward)
                new_score = 0


    my_db.users.update({'email': session['user']},
                       {
                        '$set': {
                            'score': new_score,
                            'donations': user['donations'],
                            'rewards': user['rewards']
                        }
                       })

    return jsonify({'status': 'updated'})

@main.route('/admin')
@login_required
def admin():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    all_users = my_db.users.find()

    formatted_users = []
    for user in all_users:
        clothes_count, furniture_count, books_count, electronics_count, other_count = 0, 0, 0, 0, 0
        cost_sum = 0
        cost_count = 0
        for donation in user['donations']:
            if(donation['pollAnswers']['what']['clothes']):
                clothes_count += 1
            if(donation['pollAnswers']['what']['furniture']):
                furniture_count += 1
            if(donation['pollAnswers']['what']['books']):
                books_count += 1
            if(donation['pollAnswers']['what']['electronics']):
                electronics_count += 1
            if(donation['pollAnswers']['what']['other']):
                other_count += 1

            if(donation['pollAnswers']['value']):
                cost_sum += float(donation['pollAnswers']['value'])

            cost_count += 1

        formatted_user = '''
            <div class="user">
                <div class="fname-e user-list-entry">
                    {fname}
                </div><div class="lname-e user-list-entry">
                    {lname}
                </div><div class="pnum-e user-list-entry">
                    {pnum}
                </div><div class="clothes-e user-list-entry">
                    {clothes}
                </div><div class="furniture-e user-list-entry">
                    {furniture}
                </div><div class="books-e user-list-entry">
                    {books}
                </div><div class="electronics-e user-list-entry">
                    {electronics}
                </div><div class="other-e user-list-entry">
                    {other}
                </div><div class="avg-cost-e user-list-entry">
                    {avg_cost}
                </div>
            </div>
            '''.format(fname=user['fname'], lname=user['lname'],
                       pnum=user['pnum'], clothes=clothes_count,
                       furniture=furniture_count, books=books_count,
                       electronics=electronics_count, other=other_count,
                       avg_cost=cost_sum/cost_count)
        formatted_users.append(formatted_user)

    
    return render_template('admin.html', users=''.join(formatted_users))

@main.route('/add_donation', methods=['POST'])
def add_donation():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    data = request.form
    user_exists = my_db.users.find_one({'pnum': data['pnum']})

    if(not(user_exists)):
        abort(404)

    new_score = 0

    reward_pool = ['15% off next purchase', '$5 gift card',
                   '10% next purchase']

    if(user_exists['score'] + 10 >= 100):
        new_reward = {
            'timestamp': datetime.datetime.now(),
            'code': str(uuid.uuid4())[:4],
            'desc': random.choice(reward_pool),
            'pnum': data['pnum'],
            'id': str(uuid.uuid4())
        }

        my_db.rewards.insert(new_reward)
        user_exists['rewards'].append(new_reward)
    else:
        new_score = user_exists['score'] + 10

    user_exists['donations'].append({
            'timestamp': datetime.datetime.now(),
            'pollAnswers': {
                'what': {
                    'clothes': False,
                    'furniture': False,
                    'books': False,
                    'electronics': False,
                    'other': False
                },
                'value': None
            },
            'id': str(uuid.uuid4())
        })
    

    my_db.users.update({'pnum': data['pnum']},
                       {
                        '$set': {
                            'score': new_score,
                            'donations': user_exists['donations'],
                            'rewards': user_exists['rewards']
                        }
                       })

    return jsonify({'status': 'donation added'})

@main.route('/redeem_code', methods=['POST'])
@login_required
def redeem_code():
    my_db = pymongo.MongoClient(app.config['MONGO_URL']).cfg18_dev_db

    data = request.form

    code = my_db.rewards.find_one({
            '$and': [
                {'pnum': data['pnum']},
                {'code': data['code']}
            ]
        })

    if(not(code)):
        abort(404)

    my_db.rewards.remove({
            '$and': [
                {'pnum': data['pnum']},
                {'code': data['code']}
            ]
        })

    return jsonify({'status': 'redeemed successfully'})

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
            'score': 0,
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

