from flask import Blueprint, flash, redirect, url_for, request, session, jsonify
from models.main_rou_imp_db import User
from models.imp import db
from datetime import datetime
import requests
import os
import secrets
from config import Config
from urllib.parse import urlencode

github_oauth_bp = Blueprint('github_oauth', __name__)

# GitHub OAuth2 configuration
GITHUB_CLIENT_ID = Config.GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET = Config.GITHUB_CLIENT_SECRET
GITHUB_REDIRECT_URI = Config.GITHUB_REDIRECT_URI

# GitHub OAuth2 URLs
GITHUB_AUTHORIZE_URL = Config.GITHUB_AUTHORIZE_URL
GITHUB_TOKEN_URL = Config.GITHUB_TOKEN_URL
GITHUB_USER_URL = Config.GITHUB_USER_URL
GITHUB_EMAILS_URL = Config.GITHUB_EMAILS_URL

@github_oauth_bp.route('/auth/github')
def github_login():
    """Инициализация GitHub OAuth2 авторизации"""
    # Создаем state для безопасности
    state = secrets.token_urlsafe(32)
    session['github_state'] = state
    
    # Сохраняем информацию о том, откуда пришел пользователь (для улучшения UX)
    referrer = request.referrer or ''
    if '/register' in referrer:
        session['github_action'] = 'register'
    else:
        session['github_action'] = 'login'
    
    # Параметры для авторизации GitHub
    params = {
        'client_id': GITHUB_CLIENT_ID,
        'redirect_uri': GITHUB_REDIRECT_URI,
        'scope': 'user:email',
        'state': state,
        'allow_signup': 'true'
    }
    
    # Создаем URL для авторизации
    auth_url = f"{GITHUB_AUTHORIZE_URL}?{urlencode(params)}"
    
    return redirect(auth_url)

@github_oauth_bp.route('/auth/github/callback')
def github_callback():
    """Обработка callback от GitHub"""
    # Проверяем state для безопасности
    state = request.args.get('state')
    if not state or state != session.get('github_state'):
        flash('Ошибка безопасности. Попробуйте войти снова.', 'error')
        return redirect(url_for('login_bpp.login'))
    
    # Очищаем state из сессии
    session.pop('github_state', None)
    
    # Получаем код авторизации
    code = request.args.get('code')
    if not code:
        flash('GitHub авторизация не удалась.', 'error')
        return redirect(url_for('login_bpp.login'))
    
    # Обмениваем код на access token
    token_data = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': GITHUB_REDIRECT_URI,
    }
    
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'CraftNode'
    }
    
    try:
        # Получаем access token
        token_response = requests.post(GITHUB_TOKEN_URL, data=token_data, headers=headers)
        token_response.raise_for_status()
        token_json = token_response.json()
        
        if 'error' in token_json:
            flash(f'Ошибка получения токена: {token_json.get("error_description", "Unknown error")}', 'error')
            return redirect(url_for('login_bpp.login'))
        
        access_token = token_json.get('access_token')
        if not access_token:
            flash('Не удалось получить токен доступа от GitHub.', 'error')
            return redirect(url_for('login_bpp.login'))
        
        # Получаем информацию о пользователе
        user_headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/json',
            'User-Agent': 'Love-Code-Bot-Platform'
        }
        
        # Получаем основную информацию о пользователе
        user_response = requests.get(GITHUB_USER_URL, headers=user_headers)
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Получаем email пользователя
        emails_response = requests.get(GITHUB_EMAILS_URL, headers=user_headers)
        emails_response.raise_for_status()
        emails_data = emails_response.json()
        
        # Находим основной email
        primary_email = None
        for email_info in emails_data:
            if email_info.get('primary', False):
                primary_email = email_info.get('email')
                break
        
        # Если основной email не найден, берем первый доступный
        if not primary_email and emails_data:
            primary_email = emails_data[0].get('email')
        
        # Если email все еще не найден, используем email из профиля (может быть None)
        if not primary_email:
            primary_email = user_data.get('email')
        
        if not primary_email:
            flash('GitHub не предоставил ваш email. Пожалуйста, убедитесь, что ваш email публичен в настройках GitHub.', 'error')
            return redirect(url_for('login_bpp.login'))
        
        # Получаем данные пользователя
        github_id = user_data.get('id')
        login = user_data.get('login')
        name = user_data.get('name') or login
        avatar_url = user_data.get('avatar_url')
        
        # Ищем существующего пользователя
        user = User.query.filter_by(email=primary_email).first()
        
        # Получаем действие (login или register) из сессии
        action = session.pop('github_action', 'login')
        
        if not user:
            # Создаем нового пользователя
            # Проверяем, не занят ли username
            username = login
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{login}_{counter}"
                counter += 1
            
            user = User(
                username=username,
                email=primary_email,
                role='user'
            )
            # Устанавливаем случайный пароль (пользователь не будет его знать)
            user.set_password(os.urandom(32).hex())
            
            db.session.add(user)
            db.session.commit()
            
            if action == 'register':
                flash(f'🎉 Регистрация успешна! Добро пожаловать, {username}!', 'success')
            else:
                flash(f'✅ Аккаунт создан через GitHub. Добро пожаловать!', 'success')
        else:
            if action == 'register':
                flash(f'👋 У вас уже есть аккаунт! Добро пожаловать обратно, {user.username}!', 'info')
            else:
                flash(f'🎯 Вход выполнен успешно! Привет, {user.username}!', 'success')
        
        # Авторизуем пользователя
        session.permanent = True
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return redirect(url_for('homes_bpp.home'))
        
    except requests.exceptions.RequestException as e:
        flash(f'Ошибка при связи с GitHub: {str(e)}', 'error')
        return redirect(url_for('login_bpp.login'))
    except Exception as e:
        flash(f'Произошла ошибка: {str(e)}', 'error')
        return redirect(url_for('login_bpp.login'))

@github_oauth_bp.route('/auth/github/link', methods=['POST'])
def link_github_account():
    
    return jsonify({'message': 'Функция в разработке'}), 501

@github_oauth_bp.route('/auth/github/unlink', methods=['POST'])  
def unlink_github_account():
    
    # Здесь можно добавить логику для отвязки GitHub аккаунта
    return jsonify({'message': 'Функция в разработке'}), 501