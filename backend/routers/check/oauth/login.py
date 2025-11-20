from flask import (
    Blueprint, 
    request, 
    jsonify, 
    session, 
    redirect, 
    url_for, 
    render_template
)
from models.main_rou_imp_db import User

login_bpp = Blueprint('login_bpp', __name__)

@login_bpp.route('/login', methods=['GET', 'POST'])
def login():
    """ Добавляем логику для логина юзера """
    if request.method == 'POST':
        """ Добавляем логику для логина юзера """
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = username
            session['email'] = user.email
            from flask import current_app
            current_app.logger.info(f'Regular login: User {username} logged in successfully, session: {dict(session)}')
            return redirect(url_for('homess_bpp.home'))
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    return render_template('login.html')