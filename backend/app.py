from flask import Flask
from config import Config
from import_router_bp import *
from import_all_bp import register_blueprints
from models.imp import db
from models.main_rou_imp_db import *
import os 
import logging
import swagger_ui


app = Flask(__name__, 
                    static_folder='../frontend/static', 
                    template_folder='../frontend/templates')

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(level=Config.LOG_LEVEL, filename=Config.LOG_FILE,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app.config.from_object(Config)

register_blueprints(app)

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.IP, port=Config.PORT)