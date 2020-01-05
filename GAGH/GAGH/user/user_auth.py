from functools import wraps

import bcrypt
import sqlite3 as sql

from GAGH import app
from GAGH.data.data import query_db

from flask import session, redirect, url_for, flash


def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.get('logged_in', False)
        if not status:
            return redirect(url_for('main.root'))
        return f(*args, **kwargs)

    return decorated


def get_user(email):
    try:
        result = query_db("SELECT email,hash_password FROM User WHERE email = ?", [email], one=True)
        # app.logger.info('Successfully retrieved user '+result['email'])
        # app.logger.info('Result length: '+result.len())

    except sql.Error as error:
        app.logger.error('Error retrieving user/user ' + email + ' not found: ' + str(error))
    finally:
        return result


def log_user_in(email, password):
    # app.logger.info('Email passed to user login: '+email)
    if check_auth(email, password):
        session['logged_in'] = True
        session['user'] = email

        flash('Successfully logged in')

    return


def check_auth(email, password):
    app.logger.info('Checking user auth')

    result = get_user(email)

    if result is None:
        message = 'User ' + email + ' not found'
        flash(message)
        app.logger.error(message)
        return False
    elif result['hash_password'] == bcrypt.hashpw(password.encode('UTF-8'), result['hash_password']):
        # app.logger.info('Correct password for user '+email)
        return True
    else:
        flash('Wrong password entered')
        app.logger.error('Wrong password for user ' + email)
        return False
