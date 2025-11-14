from flask import Flask
from config import Config
from models.imp import db
from models.main_rou_imp_db import *
import os 
import logging
from import_all_bp import register_blueprints
from import_router_bp import *

app = Flask(__name__, 
                    static_folder='../frontend/static', 
                    template_folder='../frontend/templates')

app.config.from_object(Config)

register_blueprints(app)

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.IP, port=Config.PORT)