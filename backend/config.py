import os
import logging
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


    IP = os.getenv("IP")
    PORT = os.getenv("PORT")
    DEBUG = os.getenv("DEBUG")

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