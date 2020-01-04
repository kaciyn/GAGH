from flask import Blueprint

# Set up a Blueprint
# bp = Blueprint('main', __name__,
#                template_folder='templates',
#                static_folder='static')

bp = Blueprint('main', __name__)

from flask import render_template


@bp.route('/')
def root():
    # need to figure out how to render this on Every one as i'm never just using the base template
    # login_status='Not logged in'
    # if session.get('logged_in',None):
    #     login_status='Logged in as: '+session['user_name']
    # return render_template('base.html',login_status=login_status),200
    return render_template('home.html'), 200


