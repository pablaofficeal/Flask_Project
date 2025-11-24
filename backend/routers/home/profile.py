from flask import Blueprint, render_template
from datetime import datetime
from models.main_rou_imp_db import User
from models.imp import db

profile_bpp = Blueprint('profile', __name__)

@profile_bpp.route('/profile')
def profile():
    user = User.query.first()
    if not user:
        return render_template('profile.html', user=None, datetime=datetime.now())

    return render_template('profile.html', user=user, datetime=datetime.now())
