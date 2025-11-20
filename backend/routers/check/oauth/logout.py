from flask import Blueprint, session, redirect, url_for

logout_bpp = Blueprint('logout_bpp', __name__)

@logout_bpp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bpp.index')) 