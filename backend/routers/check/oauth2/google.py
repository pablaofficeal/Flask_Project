from flask_dance.contrib.google import make_google_blueprint, google
from flask import Blueprint, flash, redirect, url_for, request, session
from models.main_rou_imp_db import User
from datetime import datetime
from models.imp import db
import os
from config import Config


oauth_bpp = Blueprint('oauth_bpp', __name__)
# === Google OAuth Blueprint ===
google_bp = make_google_blueprint(
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email"
    ],
    redirect_url="/google_login/callback",
    reprompt_consent=True  # всегда запрашивает токен заново
)
oauth_bpp.register_blueprint(google_bp, url_prefix="/google_login")

# Добавляем маршрут для инициации Google OAuth с сохранением контекста
@oauth_bpp.route('/google_login')
def google_login_init():
    """Инициация Google OAuth с сохранением контекста"""
    # Сохраняем информацию о том, откуда пришел пользователь (для улучшения UX)
    referrer = request.referrer or ''
    if '/register' in referrer:
        session['google_action'] = 'register'
    else:
        session['google_action'] = 'login'
    
    # Перенаправляем на стандартный Google OAuth
    return redirect(url_for('oauth_bpp.google.login'))

# === Google OAuth Login Route ===
@oauth_bpp.route('/google_login/callback')
def google_callback():
    if not google.authorized:
        flash("Google авторизация не удалась.", 'error')
        return redirect(url_for('login_bpp.login'))

    try:
        resp = google.get("/oauth2/v2/userinfo")
    except Exception as e:
        # Ловим просроченный токен и удаляем сессию
        session.clear()
        flash("Срок действия Google-токена истёк. Попробуй снова.", 'error')
        return redirect(url_for('login_bpp.login'))

    if not resp.ok:
        flash("Ошибка при получении данных из Google.", 'error')
        return redirect(url_for('login_bpp.login'))

    info = resp.json()
    email = info.get("email")
    username = info.get("name") or email.split("@")[0]

    if not email:
        flash("Google не вернул email.", 'error')
        return redirect(url_for('login_bpp.login'))

    # Получаем действие (login или register) из сессии
    action = session.pop('google_action', 'login')
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # Проверяем, не занят ли username
        original_username = username
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{original_username}_{counter}"
            counter += 1
        
        user = User(username=username, email=email)
        user.set_password(os.urandom(32).hex())
        db.session.add(user)
        db.session.commit()
        
        if action == 'register':
            flash(f'🎉 Регистрация успешна! Добро пожаловать, {username}!', 'success')
        else:
            flash(f'✅ Аккаунт создан через Google. Добро пожаловать!', 'success')
    else:
        if action == 'register':
            flash(f'👋 У вас уже есть аккаунт! Добро пожаловать обратно, {user.username}!', 'info')
        else:
            flash(f'🎯 Вход выполнен успешно! Привет, {user.username}!', 'success')

    session.permanent = True
    session['user_id'] = user.id
    session['username'] = user.username
    session['email'] = user.email
    user.last_login = datetime.utcnow()
    db.session.commit()

    return redirect(url_for('homess_bpp.home'))