from flask import Flask, g,render_template,request

import sqlite3 as sql,ConfigParser

app=Flask(__name__)

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

@app.route('/test/')
def test():
    try:
        reviewer_id = 'ksdjhf'
        barbershop_id = 'lsdkfjlksdjf'
        date_visited = 58937
        date_added = 2340598
        title = 'aaaaaa'
        review_text = 'sdfgsdfgsdfgdsfgsdfg'
        haircut_rating = 5
        anxiety_rating = 3
        friendliness_rating = 1
        pricerange = 2
     
        gender_remarks = 1
        gender_charged = 1
        unsafe = 0

        db.cursor().execute("INSERT INTO Review (reviewer_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(reviewer_id,barbershop_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe) )
        db.commit()
        msg = "Record successfully added"
    except:
        db.rollback()
        msg = "error in insert operation"
      
    finally:
        list(msg)

@app.route('/submit/submit-review',methods = ['POST', 'GET'])
def submit_review():
    msg=''
    db = get_db()
    if request.method == 'POST':
        try:
        	reviewer_id = request.form['email']
            barbershop_id = request.form['barbershop_id']
            date_visited = request.form['date_visited']
            date_added = request.form['date_added']
            title = request.form['title']
            review_text = request.form['review_text']
            haircut_rating = request.form['haircut_quality']
            anxiety_rating = request.form['anxiety']
            friendliness_rating = request.form['friendliness']
            pricerange = request.form['price']
            # barber_id = request.form['barber_id']
            # barber_recommended = request.form['barber_recommended']
            gender_remarks = request.form['gender_remarks']
            gender_charged = request.form['gender_charged']
            unsafe = request.form['unsafe']

            db.cursor().execute("INSERT INTO Review (reviewer_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(reviewer_id,barbershop_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe) )
            db.commit()
            msg = "Record successfully added"
        except:
            db.rollback()
            msg = "error in insert operation"
      
        finally:
            list(msg)

def list(msg):
    db = get_db()

    page = []
    page.append('<html><ul>')
    sql = "SELECT * FROM Review ORDER BY barbershop_id"
    for row in db.cursor().execute(sql):
        page.append('<li>')
        page.append(str(row))
        page.append('</li>')
        page.append(msg)
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

def init(app):
    config = ConfigParser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")

    except:
        print "Could not read configs from: ", config_location

init(app)


if __name__ == "__main__":
    init(app)
    app.run(
        host=app.config['ip_address'],
        port=int(app.config['port']))
