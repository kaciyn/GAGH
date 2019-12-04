import sys,os,sqlite3 as sql,configparser,logging,time,bcrypt
from datetime import datetime

from flask import Flask,g,render_template,request, url_for,session, redirect, flash
# you need to uh actually. flash the messages
from logging.handlers import RotatingFileHandler
from functools import wraps



app=Flask(__name__)
app.secret_key=os.urandom(24)

db_location='var/GAGH.db'
html_location='static/html/'

#requires login decorator, copied wholesale from workbook
def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.get('logged_in', False)
        if not status:
            return redirect(url_for('.root'))
        return f(*args, **kwargs)
    return decorated

#PAGES
@app.route('/')
def root():
    # need to figure out how to render this on Every one as i'm never just using the base template
    # login_status='Not logged in'
    # if session.get('logged_in',None):
    #     login_status='Logged in as: '+session['user_name']
    #return render_template('base.html',login_status=login_status),200
    return render_template('home.html'),200

#SUBMIT
@app.route("/submit/")
@requires_login
def new_review():
   return render_template('submit.html')
    
@app.route('/submit/submit-review/',methods = ['POST', 'GET'])
@requires_login
def submit_review():
    db = get_db()
    if request.method == 'POST':
        try:
            app.logger.info('Barbershop id received: '+request.form.get('barbershop_id'))
            #placeholder til i figure out a way to get gmaps to send me shit
            barbershop_id='sdjkfhs'
            barbershop_name='Stag Barbers'
            barbershop_address='22 Lady Lawson St, Edinburgh EH3 9DS'

            reviewer_id = session['user']

            #barbershop_id = request.form.get('barbershop_id')
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
            
            db.cursor().execute('INSERT INTO Review (reviewer_id,barbershop_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',(reviewer_id,barbershop_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe))


            #if the barbershop is new
            if query_db("SELECT placeID FROM Barbershop WHERE placeID = ?",[barbershop_id],one=True) is None:
                db.cursor().execute('INSERT INTO Barbershop (placeID,name,address) VALUES (?,?,?)',(barbershop_id,barbershop_name,barbershop_address))
                app.logger.info('New barbershop '+barbershop_name+' added to db')


            db.commit()
            app.logger.info('Successfully committed review for '+barbershop_name+' to db')
            flash('Review submitted!') 
            return redirect(url_for('.review_submitted'))
        except sql.Error as error:
            db.rollback()
            app.logger.error("Error in insert operation: "+str(error))   
            return redirect(url_for('.submit_error'))
     

@app.route('/submit/review-submitted/')
@requires_login
def review_submitted():
    return render_template('review-submitted.html')

@app.route('/submit/error/')
@requires_login
def submit_error():
    return render_template('submit-error.html')


#USER LOGINS, partially adapted from workbook
@app.route('/register/')
def register():
    return render_template('newuser.html')

@app.route('/register/newuser/',methods = ['POST', 'GET'])
def newuser():
    email = request.form['email'].lower().strip()
    password=request.form['password'].strip()
    if request.method == 'POST':
        #if user doesn't already exist
        if get_user(email) is None:
            try:
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                name = request.form['name'].strip()
                location = request.form['location'].strip()
                
                db = get_db()

                db.cursor().execute("INSERT INTO User (email,hash_password,name,location) VALUES (?,?,?,?)",(email,hash_password,name,location) )

                db.commit()
                app.logger.info('Successfully added user '+email+' to db')

               return user_login(email,password)

            except sql.Error as error:
                db.rollback()
                app.logger.error('Error in user '+email+' insert operation: '+str(error))     
        else:
            app.logger.error('User'+email+' already exists!')
            return redirect(url_for('.register'))
            #if you have time (you don't) send the old user details back to the form, or flash an error message and stay on the page

@app.route('/newusersuccess/')
@requires_login
def newusersuccess():
    return render_template('newusersuccess.html')

def get_user(email):
    try:
        result=query_db("SELECT email,hash_password FROM User WHERE email = ?",[email],one=True)
        #app.logger.info('Successfully retrieved user '+result['email'])
        #app.logger.info('Result length: '+result.len())
    
    except sql.Error as error:
        app.logger.error('Error retrieving user/user '+email+' not found: '+str(error))
    finally:
        return result

@app.route('/login/',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password'].strip()
        #app.logger.info("Login requested for: "+email)
        
        return user_login(email,password)
  

def user_login(email,password):         
    #app.logger.info('Email passed to user login: '+email)
    if check_auth(email,password):
        session['logged_in'] = True
        session['user']=email

        flash('Successfully logged in')

    return redirect(url_for('.root'))


def check_auth(email, password):
    result=get_user(email)

    if(result is None):
        message='User '+email+' not found'
        flash(message)
        app.logger.error(message)
        return False
    elif (result['hash_password'] == bcrypt.hashpw(password.encode('utf-8'), result['hash_password'])):
        #app.logger.info('Correct password for user '+email)
        return True
    else:
        flash('Wrong password entered')
        app.logger.error('Wrong password for user '+email)
        return False

@app.route('/user/')
@requires_login
def user():
    user=query_db("SELECT email,name,location FROM User WHERE email = ?",[session['user']],one=True)
    
    if user is None:
        return redirect(url_for('.root'))

    if session.get('user_name', None) is None:
        session['user_name']=user['name']

    return render_template('user.html',user=user)

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    session['user']= None
    session['user_name']= None
    app.logger.info('Logged out')
    return redirect(url_for('.root'))


@app.route('/barbershops/')
def barbershops():
    #selects barbershop infos 

    barbershops=query_db(" SELECT b.placeid, b.NAME, b.address, b.known_friendly, Avg(r.haircut_rating) AS haircut_rating_average, Avg(r.anxiety_rating) AS anxiety_rating_average, Avg(r.friendliness_rating) AS friendliness_rating_average, (AVG(r.unsafe)*100) AS unsafe_average, (AVG(r.gender_remarks)*100) AS gender_remarks_average, (AVG(r.gender_charged)*100) AS gender_charged_average, Count(*) AS review_count FROM barbershop AS b INNER JOIN review AS r ON r.barbershop_id = b.placeid GROUP BY b.placeid ORDER BY unsafe_average ASC")
    return render_template('barbershops.html',barbershops=barbershops)

@app.route('/reviews/')
def reviews():
    return render_template('comingsoon.html')

@app.route('/faq/')
def faq():
    return render_template('comingsoon.html')

@app.route('/about/')
def about():
    return render_template('about.html')


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
#from https://flask.palletsprojects.com/en/0.12.x/patterns/sqlite3/#easy-querying
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sql.connect(db_location)
        g.db = db
        db.row_factory = sql.Row

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
