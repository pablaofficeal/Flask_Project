from flask import Blueprint, render_template
from models.main_rou_imp_db import User, Post
from models.imp import db

homes_bpp = Blueprint('homes_bpp', __name__)

@homes_bpp.route('/home')
def home():
    user = User.query.first()
    if not user:
        return render_template('home.html', user=None)
        posts = None
    else:
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    
    return render_template('home.html', user=user, posts=posts)
# делаем костомную страницу с ошибкуй 500
@homes_bpp.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500
