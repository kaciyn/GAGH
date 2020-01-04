from flask import render_template

from GAGH import app
from GAGH import query_db


@app.route('/barbershops/')
def barbershops():
    # selects barbershop infos

    barbershops = query_db(
        " SELECT b.placeid, b.NAME, b.address, b.known_friendly, Avg(r.haircut_rating) AS haircut_rating_average, Avg(r.anxiety_rating) AS anxiety_rating_average, Avg(r.friendliness_rating) AS friendliness_rating_average, (AVG(r.unsafe)*100) AS unsafe_average, (AVG(r.gender_remarks)*100) AS gender_remarks_average, (AVG(r.gender_charged)*100) AS gender_charged_average, Count(*) AS review_count FROM barbershop AS b INNER JOIN review AS r ON r.barbershop_id = b.placeid GROUP BY b.placeid ORDER BY unsafe_average ASC")
    return render_template('barbershops.html', barbershops=barbershops)


@app.route('/reviews/')
def reviews():
    return render_template('comingsoon.html')
