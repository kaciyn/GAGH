import sys
import os
import sqlite3 as sql,configparser
import logging
from datetime import datetime
import time
import bcrypt

from flask import Flask,g,render_template,request, url_for,session, redirect
from logging.handlers import RotatingFileHandler
from functools import wraps



app=Flask(__name__)
app.secret_key=os.urandom(24)

db_location='var/GAGH.db'
html_location='static/html/'

#PAGES
@app.route('/')
def root():
	return render_template('base.html'),200

#SUBMIT
@app.route("/submit/")
def new_review():
   return render_template('submit.html')
    
@app.route('/submit/submit-review/',methods = ['POST', 'GET'])
def submit_review():
    db = get_db()
    if request.method == 'POST':
        try:
            reviewer_id = request.form.get('reviewer_id')

            barbershop_id = request.form.get('barbershop_id')
            date_visited = int(request.form.get('date_visited').replace('-',''))

            date_added = int(round(time.time() * 1000))
            title = request.form.get('title')
            review_text = request.form.get('review')
            haircut_rating = request.form.get('haircut_quality')

            anxiety_rating = request.form.get('anxiety')
            friendliness_rating = request.form.get('friendliness')
            pricerange = request.form.get('price')
            # barber_id = request.form.get('barber_id')
            # barber_recommended = request.form.get('barber_recommended')
            gender_remarks = request.form.get('gender_remarks')
            
            gender_charged = request.form.get('gender_charged')
            unsafe = request.form.get('unsafe')
            
            db.cursor().execute("INSERT INTO Review (reviewer_id,barbershop_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(reviewer_id,barbershop_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe) )

            db.commit()
            app.logger.info('Successfully committed review to db')
        except sql.Error as error:
            db.rollback()
            app.logger.error("Error in insert operation: "+str(error))     
        finally:
           return list()

def list():
    db = get_db()

    page = []
    page.append('<html><ul>')
    sql = "SELECT * FROM Review ORDER BY barbershop_id"
    for row in db.cursor().execute(sql):
        page.append('<li>')
        page.append(str(row))
        page.append('</li>')
        page.append('</ul><html>')
    return ''.join(page)


#USER LOGINS, partially adapted from workbook
@app.route('/register/')
def register():
    return render_template('newuser.html')

@app.route('/register/newuser',methods = ['POST', 'GET'])
def newuser():
    db = get_db()

    if request.method == 'POST':
        new_user=request.form.get('user')
        new_user_password=request.form.get('password')


        #if user already exists
        if get_user(new_user)==None:
            try:
                db.cursor().execute("SELECT email,hash_password FROM User WHERE email = (?)",(email))
                result=db.cursor().fetchall
                app.logger.info('Successfully retrieved user')

                user = request.form['email']
                password=request.form['password']
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                name = request.form['name']
                location = request.form['location']

                db.cursor().execute("INSERT INTO User (email,hash_password,name,location) VALUES (?,?,?,?)",(email,hash_password,name) )

                db.commit()
                app.logger.info('Successfully added user to db')
            except sql.Error as error:
                db.rollback()
                app.logger.error("Error in user insert operation: "+str(error))     
            finally:
                user_login(email,password)
        else:
            app.logger.error('User'+new_user+' already exists!')
            register()
            #if you have time send the old user details back to the form, or flash an error message and stay on the page

@app.route('/user/')
def user():
    return render_template('user.html')


@app.route('/login/',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['email']
        password = request.form['password']

        return user_login(user,password)
  

def user_login(email,password):         
    if check_auth(email,password):
        session['logged_in'] = True
        return redirect(url_for('.secret'))


def check_auth(email, password):
    result=get_user(email)

    if(email==None):
        app.logger.error("User not found")
        return False
    if(email == result.email):
        if (result.hash_password == bcrypt.hashpw(password.encode('utf-8'), result.hash_password)):
            return True
        else:
            app.logger.error("Wrong password")
            return False
    else:
        app.logger.error("User not found")
        return False
  

def get_user(email):
    db = get_db()
    db.row_factory = sql.Row

    try:
        db.cursor().execute("SELECT email,hash_password FROM User WHERE email = ?",email)
        result=db.cursor().fetchall
        app.logger.info('Successfully retrieved user')
    except sql.Error as error:
        app.logger.error("Error retrieving user/user not found: "+str(error))
        result=None
    finally:
        return result


def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.get('logged_in', False)
        if not status:
            return redirect(url_for('.root'))
        return f(*args, **kwargs)
    return decorated

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('.root'))

@app.route("/secret/")
@requires_login
def secret():
    return "Secret Page"


#LOGGING
def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_pathname, maxBytes=1024* 1024 * 10 , backupCount=1024)
    file_handler.setLevel( app.config['log_level'] )
    formatter = logging.Formatter("%(levelname)s | %(asctime)s |  %(module)s | %(funcName)s | %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.setLevel( app.config['log_level'] )
    app.logger.addHandler(file_handler)

#DATABASE
def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sql.connect(db_location)
        g.db = db
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#INIT
def init(app):
    config = configparser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")

        app.config['log_file'] = config.get("logging", "name")
        app.config['log_location'] = config.get("logging", "location")
        app.config['log_level'] = config.get("logging", "level")

    except:
        app.logger.error ("Could not read configs from: ", config_location)



init(app)
logs(app)


if __name__ == "__main__":
    init(app)
    logs(app)

    app.run(
        host=app.config['ip_address'],
        port=int(app.config['port']))
