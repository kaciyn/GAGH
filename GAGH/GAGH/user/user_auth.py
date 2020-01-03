import sqlite3 as sql, bcrypt

from flask import render_template, request, url_for, session, redirect, flash
from functools import wraps

# requires login decorator, copied wholesale from workbook
from GAGH import app
from GAGH.GAGH.data.data import get_db, query_db


def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.get('logged_in', False)
        if not status:
            return redirect(url_for('.root'))
        return f(*args, **kwargs)

    return decorated



# USER LOGINS, partially adapted from workbook
@app.route('/register/')
def register():
    return render_template('newuser.html')


@app.route('/register/newuser/', methods=['POST', 'GET'])
def newuser():
    email = request.form['email'].lower().strip()
    password = request.form['password'].strip()
    if request.method == 'POST':
        # if user doesn't already exist
        if get_user(email) is None:
            try:
                hash_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
                name = request.form['name'].strip()
                location = request.form['location'].strip()

                db = get_db()

                db.cursor().execute("INSERT INTO User (email,hash_password,name,location) VALUES (?,?,?,?)",
                                    (email, hash_password, name, location))

                db.commit()
                app.logger.info('Successfully added user ' + email + ' to db')

                return log_user_in(email, password)

            except sql.Error as error:
                db.rollback()
                app.logger.error('Error in user ' + email + ' insert operation: ' + str(error))
        else:
            app.logger.error('User' + email + ' already exists!')
            return redirect(url_for('.register'))
            # if you have time (you don't) send the old user details back to the form, or flash an error message and stay on the page


@app.route('/newusersuccess/')
@requires_login
def newusersuccess():
    return render_template('newusersuccess.html')


def get_user(email):
    try:
        result = query_db("SELECT email,hash_password FROM User WHERE email = ?", [email], one=True)
        # app.logger.info('Successfully retrieved user '+result['email'])
        # app.logger.info('Result length: '+result.len())

    except sql.Error as error:
        app.logger.error('Error retrieving user/user ' + email + ' not found: ' + str(error))
    finally:
        return result


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password'].strip()
        # app.logger.info("Login requested for: "+email)

        return log_user_in(email, password)


def log_user_in(email, password):
    # app.logger.info('Email passed to user login: '+email)
    if check_auth(email, password):
        session['logged_in'] = True
        session['user'] = email

        flash('Successfully logged in')

    return redirect(url_for('.root'))


def check_auth(email, password):
    app.logger.info('Checking user auth')

    result = get_user(email)

    if (result is None):
        message = 'User ' + email + ' not found'
        flash(message)
        app.logger.error(message)
        return False
    elif (result['hash_password'] == bcrypt.hashpw(password.encode('UTF-8'), result['hash_password'])):
        # app.logger.info('Correct password for user '+email)
        return True
    else:
        flash('Wrong password entered')
        app.logger.error('Wrong password for user ' + email)
        return False


@app.route('/user/')
@requires_login
def user():
    user = query_db("SELECT email,name,location FROM User WHERE email = ?", [session['user']], one=True)

    if user is None:
        return redirect(url_for('.root'))

    if session.get('user_name', None) is None:
        session['user_name'] = user['name']

    return render_template('user.html', user=user)


@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    print('Logging user:' + session['user'] + ' out')
    app.logger.info('Logging user:' + session['user'] + ' out')
    session['logged_in'] = False
    session['user'] = None
    session['user_name'] = None
    app.logger.info('Logged out')
    return redirect(url_for('.root'))
