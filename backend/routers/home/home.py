from flask import Blueprint, render_template
from models.main_rou_imp_db import User
from models.imp import db

homes_bpp = Blueprint('homes_bpp', __name__)

@homes_bpp.route('/home')
def home():
    
    users = User.query.all()
    return render_template('home.html', users=users)