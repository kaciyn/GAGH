from flask import Flask,g,render_template,request, url_for,session
from logging.handlers import RotatingFileHandler

import sys
import os
import sqlite3 as sql,configparser
import logging
import datetime
import time

app=Flask(__name__)
app.secret_key=os.urandom(24)

db_location='var/GAGH.db'
html_location='static/html/'

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

@app.route('/')
def root():
	return render_template('base.html'),200

@app.route("/submit/")
def new_review():
   return render_template('submit.html')
    

@app.route('/submit/submit-review/',methods = ['POST', 'GET'])
def submit_review():
    db = get_db()
    if request.method == 'POST':
        try:
            reviewer_id = request.form.get('reviewer_id')
            app.logger.info('reviewer id: '+reviewer_id)

            barbershop_id = request.form.get('barbershop_id')
            date_visited = request.form.get('date_visited')
            app.logger.info('date visited: '+str(date_visited))

            date_added = request.form.get('date_added')
            title = request.form.get('title')
            review_text = request.form.get('review')
            haircut_rating = request.form.get('haircut_quality')
            app.logger.info('haircut rating: '+haircut_rating)

            anxiety_rating = request.form.get('anxiety')
            friendliness_rating = request.form.get('friendliness')
            pricerange = request.form.get('price')
            # barber_id = request.form.get('barber_id')
            # barber_recommended = request.form.get('barber_recommended')
            gender_remarks = request.form.get('gender_remarks')
            app.logger.info('gender remarks: '+gender_remarks)
            
            gender_charged = request.form.get('gender_charged')
            unsafe = request.form.get('unsafe')

            barber_id=None
            barber_recommended=0
            
            db.cursor().execute("INSERT INTO Review (reviewer_id,barbershop_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe,barber_id,barber_recommended) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(reviewer_id,barbershop_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe,barber_id,barber_recommended) )

            db.commit()
            app.logger.info('Successfully committed review to db')
        except sql.Error as error:
            db.rollback()
            app.logger.error("Error in insert operation: "+str(error))     
        finally:
            list()

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


@app.route('/config/')
def config():
    strg = []
    strg.append('Debug: %s' % app.config['DEBUG'])
    strg.append('port:'+app.config['port'])
    strg.append('url:'+app.config['url'])
    strg.append('ip_address:'+app.config['ip_address'])
    return '\t'.join(str)

@app.route('/logtest/')
def logtest():
    app.logger.info('testing info from '+url_for('logtest'))
    app.logger.error('testing error')
    return 'testing logger'


@app.route('/formtest/')
def formtest():
   return render_template('formtest.html')

@app.route('/testresult/',methods = ['POST', 'GET'])
def testsubmit():
    db = get_db()
    if request.method == 'POST':
        friendliness_rating = request.form.get('friendliness')
        app.logger.info('Form test result: '+friendliness_rating)
        return friendliness_rating
    else: 
        return "didn't get result"


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


def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_pathname, maxBytes=1024* 1024 * 10 , backupCount=1024)
    file_handler.setLevel( app.config['log_level'] )
    formatter = logging.Formatter("%(levelname)s | %(asctime)s |  %(module)s | %(funcName)s | %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.setLevel( app.config['log_level'] )
    app.logger.addHandler(file_handler)

init(app)
logs(app)


if __name__ == "__main__":
    init(app)
    logs(app)

    app.run(
        host=app.config['ip_address'],
        port=int(app.config['port']))
