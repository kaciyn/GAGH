import  sqlite3 as sql, time

from flask import  render_template, request, url_for, session, redirect, flash
# you need to uh actually. flash the messages

# SUBMIT
from GAGH import app
from GAGH import get_db, query_db
from GAGH import requires_login


@app.route("/submit/")
@requires_login
def new_review():
    return render_template('submit.html')


@app.route('/submit/submit-review/', methods=['POST', 'GET'])
@requires_login
def submit_review():
    db = get_db()
    if request.method == 'POST':
        try:
            app.logger.info('Barbershop id received: ' + request.form.get('placeID'))
            # placeholder til i figure out a way to get gmaps to send me shit
            barbershop_id = request.form.get('placeID')
            barbershop_name = request.form.get('name')
            barbershop_address = request.form.get('address')

            reviewer_id = session['user']

            # barbershop_id = request.form.get('barbershop_id')
            date_visited = int(request.form.get('date_visited').replace('-', ''))

            date_added = int(round(time.time() * 1000))
            title = request.form.get('title')
            review_text = request.form.get('review')
            haircut_rating = request.form.get('haircut_quality')

            anxiety_rating = request.form.get('anxiety')
            friendliness_rating = request.form.get('friendliness')
            pricerange = request.form.get('price') or 0
            # barber_id = request.form.get('barber_id')
            # barber_recommended = request.form.get('barber_recommended')
            gender_remarks = request.form.get('gender_remarks') or 0

            gender_charged = request.form.get('gender_charged') or 0

            unsafe = request.form.get('unsafe') or 0

            db.cursor().execute(
                'INSERT INTO Review (reviewer_id,barbershop_id,date_visited,date_added,title,review_text,haircut_rating,anxiety_rating,friendliness_rating,pricerange,gender_remarks,gender_charged,unsafe) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (reviewer_id, barbershop_id, date_visited, date_added, title, review_text, haircut_rating,
                 anxiety_rating, friendliness_rating, pricerange, gender_remarks, gender_charged, unsafe))

            # if the barbershop is new
            if query_db("SELECT placeID FROM Barbershop WHERE placeID = ?", [barbershop_id], one=True) is None:
                db.cursor().execute('INSERT INTO Barbershop (placeID,name,address) VALUES (?,?,?)',
                                    (barbershop_id, barbershop_name, barbershop_address))
                app.logger.info('New barbershop ' + barbershop_name + ' added to db')

            db.commit()
            app.logger.info('Successfully committed review for ' + barbershop_name + ' to db')
            flash('Review submitted!')
            return redirect(url_for('.review_submitted'))
        except sql.Error as error:
            db.rollback()
            app.logger.error("Error in insert operation: " + str(error))
            return redirect(url_for('.submit_error'))

    @app.route('/submit/review-submitted/')
    @requires_login
    def review_submitted():
        return render_template('review-submitted.html')

    @app.route('/submit/error/')
    @requires_login
    def submit_error():
        return render_template('submit-error.html')
