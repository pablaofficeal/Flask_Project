from models.imp import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(600), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, password):
        """Хэширует и устанавливает пароль для пользователя"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверяет пароль пользователя"""
        return check_password_hash(self.password, password)
    
    # Flask-Login required methods
    def is_authenticated(self):
        """Возвращает True, если пользователь аутентифицирован"""
        return True
    
    def is_active(self):
        """Возвращает True, если пользователь активен"""
        return True
    
    def is_anonymous(self):
        """Возвращает True, если пользователь анонимный"""
        return False
    
    def get_id(self):
        """Возвращает уникальный идентификатор пользователя"""
        return str(self.id)