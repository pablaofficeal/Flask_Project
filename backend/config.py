import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = "test_secret_key"

    IP = os.getenv("IP")
    PORT = os.getenv("PORT")
    DEBUG = "False"

    LOG_LEVEL = "DEBUG"
    LOG_FILE = "logs/app.log"

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

    GITHUB_AUTHORIZE_URL = os.getenv("GITHUB_AUTHORIZE_URL")
    GITHUB_TOKEN_URL = os.getenv("GITHUB_TOKEN_URL")
    GITHUB_USER_URL = os.getenv("GITHUB_USER_URL")
    GITHUB_EMAILS_URL = os.getenv("GITHUB_EMAILS_URL")
    GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")

    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_KEY = os.getenv("SESSION_COOKIE_KEY")
    SESSION_COOKIE_PATH = '/'
    SESSION_COOKIE_DOMAIN = 'localhost'

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    DEBUG = "True"


    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_KEY = os.getenv("TEST_SESSION_COOKIE_KEY")