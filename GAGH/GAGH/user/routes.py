import sqlite3 as sql, bcrypt

from flask import render_template, request, url_for, session, redirect
from flask import Blueprint

# requires login decorator, copied wholesale from workbook
from GAGH import app
from GAGH.data.data import get_db, query_db
import GAGH.user.user_auth as auth

bp = Blueprint('user', __name__)


# partially adapted from workbook
@bp.route('/register/')
def register():
    return render_template('user/new_user.html')


@bp.route('/register/newuser/', methods=['POST', 'GET'])
def newuser():
    email = request.form['email'].lower().strip()
    password = request.form['password'].strip()
    if request.method == 'POST':
        # if user doesn't already exist
        if auth.get_user(email) is None:
            try:
                hash_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
                name = request.form['name'].strip()
                location = request.form['location'].strip()

                db = get_db()

                db.cursor().execute("INSERT INTO User (email,hash_password,name,location) VALUES (?,?,?,?)",
                                    (email, hash_password, name, location))

                db.commit()
                app.logger.info('Successfully added user ' + email + ' to db')

                auth.log_user_in(email, password)

                return redirect(url_for('.new_user_success'))

            except sql.Error as error:
                db.rollback()
                app.logger.error('Error in user ' + email + ' insert operation: ' + str(error))
        else:
            app.logger.error('User' + email + ' already exists!')
            return redirect(url_for('.register'))
            # if you have time (you don't) send the old user details back to the form, or flash an error message and stay on the page


@bp.route('/new_user_success/')
@auth.requires_login
def new_user_success():
    return render_template('user/new_user_success.html')


@bp.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password'].strip()
        # app.logger.info("Login requested for: "+email)

        auth.log_user_in(email, password)

        return redirect(url_for('main.root'))


@bp.route('/user/')
@auth.requires_login
def user():
    user_info = query_db("SELECT email,name,location FROM User WHERE email = ?", [session['user']], one=True)

    if user_info is None:
        return redirect(url_for('main.root'))

    if session.get('user_name', None) is None:
        session['user_name'] = user_info['name']

    return render_template('user.html', user=user_info)


@bp.route('/logout/', methods=['POST', 'GET'])
def logout():
    print('Logging user:' + session['user'] + ' out')
    app.logger.info('Logging user:' + session['user'] + ' out')
    session['logged_in'] = False
    session['user'] = None
    session['user_name'] = None
    app.logger.info('Logged out')
    return redirect(url_for('main.root'))
