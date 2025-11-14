import os
import logging
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    

    IP = os.getenv("IP")
    PORT = os.getenv("PORT")
    DEBUG = os.getenv("DEBUG")