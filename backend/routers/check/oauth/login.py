from flask import (
    Blueprint, 
    request, 
    jsonify, 
    session, 
    redirect, 
    url_for, 
    render_template,
    flash
)
from models.main_rou_imp_db import User
from flask import current_app
from datetime import datetime
from models.imp import db



login_bpp = Blueprint('login_bpp', __name__)

@login_bpp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session.permanent = True
            user.last_login = datetime.now()
            db.session.commit()
            return redirect(url_for('homes_bpp.home'))
        else:
            flash('Invalid username or password')
            return render_template('login.html')

    return render_template('login.html')
