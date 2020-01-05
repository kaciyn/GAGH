from flask import Blueprint
from flask import render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def root():
    # need to figure out how to render this on Every one as i'm never just using the base template
    # login_status='Not logged in'
    # if session.get('logged_in',None):
    #     login_status='Logged in as: '+session['user_name']
    # return render_template('base.html',login_status=login_status),200
    return render_template('main/home.html'), 200


@bp.route('/faq/')
def faq():
    return render_template('main/comingsoon.html')


@bp.route('/about/')
def about():
    return render_template('main/about.html')