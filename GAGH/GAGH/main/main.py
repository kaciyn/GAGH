from flask import render_template

# PAGES
from GAGH import app
from GAGH.GAGH.user.user_auth import requires_login


@app.route('/')
def root():
    # need to figure out how to render this on Every one as i'm never just using the base template
    # login_status='Not logged in'
    # if session.get('logged_in',None):
    #     login_status='Logged in as: '+session['user_name']
    # return render_template('base.html',login_status=login_status),200
    return render_template('home.html'), 200


@app.route('/submit/review-submitted/')
@requires_login
def review_submitted():
    return render_template('review-submitted.html')


@app.route('/submit/error/')
@requires_login
def submit_error():
    return render_template('submit-error.html')
