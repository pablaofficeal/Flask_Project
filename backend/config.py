import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


    IP = os.getenv("IP")
    PORT = os.getenv("PORT")
    DEBUG = "False"

    LOG_LEVEL = os.getenv("LOG_LEVEL")
    LOG_FILE = os.getenv("LOG_FILE")

    # Google OAuth2 Configuration
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    # GitHub OAuth2 Configuration
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

    GITHUB_AUTHORIZE_URL = os.getenv("GITHUB_AUTHORIZE_URL")
    GITHUB_TOKEN_URL = os.getenv("GITHUB_TOKEN_URL")
    GITHUB_USER_URL = os.getenv("GITHUB_USER_URL")
    GITHUB_EMAILS_URL = os.getenv("GITHUB_EMAILS_URL")
    GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")


    # Cookies settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_NAME = 'soundrush_session'
    SESSION_COOKIE_SAMESITE = 'None'  # Изменено с 'None' на 'Lax' для лучшей совместимости
    SESSION_COOKIE_SECURE = False  # Изменено на False для development среды
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_KEY = os.getenv("SESSION_COOKIE_KEY")