from flask import Blueprint, render_template
from flask_login import current_user, login_required
from datetime import datetime

profile_bpp = Blueprint('profile', __name__)

@profile_bpp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user, datetime=datetime.now())
