from flask import Blueprint, render_template
from models.main_rou_imp_db import Post
from models.imp import db
from flask_login import current_user, login_required



home_bpp = Blueprint('home_bpp', __name__)

@home_bpp.route('/')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', user=current_user, posts=posts)
