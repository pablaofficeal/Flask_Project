from flask import Blueprint, render_template, request, redirect, url_for
from models.main_rou_imp_db import User
from datetime import datetime
from models.imp import db


register_bpp = Blueprint('register_bpp', __name__)

@register_bpp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Система регистрации нового пользователя
     ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: Имя пользователя
      - name: email
        in: formData
        type: string
        required: true
        description: Email пользователя
      - name: password
        in: formData
        type: string
        required: true
        description: Пароль пользователя
    responses:
      200:
        description: Успешная регистрация
    
      400:
        description: Неверный запрос, проверьте данные
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = User(username=username, password=password, email=email, created_at=datetime.now())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_bpp.login'))
    return render_template('register.html')