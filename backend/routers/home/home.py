from flask import Blueprint, render_template
from models.main_rou_imp_db import User, Post
from models.imp import db
from flask_login import current_user, login_required


homes_bpp = Blueprint('homes_bpp', __name__)

@homes_bpp.route('/home')
@login_required
def home():
    # Получаем все посты из базы данных
    posts = Post.query.all()
    # Получаем  пользователя из базы данных
    return render_template('home.html', user=current_user, posts=posts)
