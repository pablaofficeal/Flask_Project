from flask import Flask
from config import Config
from import_router_bp import *
from import_all_bp import register_blueprints
from models.imp import db
from models.main_rou_imp_db import *
import os 
import logging
import swagger_ui
from flask_login import LoginManager


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


# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_bpp.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

if __name__ == '__main__':
    app.run(debug=False, host=Config.IP, port=Config.PORT)