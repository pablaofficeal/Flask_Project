from flask import Blueprint, session, redirect, url_for
from flask_login import logout_user

logout_bpp = Blueprint('logout_bpp', __name__)

@logout_bpp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_bpp.index'))