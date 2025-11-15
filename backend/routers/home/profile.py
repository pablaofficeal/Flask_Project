from flask import Blueprint, render_template
from models.main_rou_imp_db import User
from models.imp import db

profile_bpp = Blueprint('profile', __name__)

@profile_bpp.route('/profile')
def profile():
    user = User.query.first()
    email = user.email if user else 'Guest'
    password = user.password if user else 'N/A'
    return render_template('profile.html', user=user, email=email, password=password)
