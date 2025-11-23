from flask import Blueprint, render_template
from models.main_rou_imp_db import Post
from models.imp import db



home_bpp = Blueprint('home_bpp', __name__)

@home_bpp.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)
