from flask import Flask
from config import Config
from models.imp import db
from models.main_rou_imp_db import *
import os 
import logging


app = Flask(__name__)
app.config = Config()
db.init_app(app)
