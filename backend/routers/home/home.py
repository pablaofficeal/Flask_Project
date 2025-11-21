from flask import Blueprint, render_template
from models.main_rou_imp_db import User, Post
from models.imp import db

homes_bpp = Blueprint('homes_bpp', __name__)

@homes_bpp.route('/home')
def home():
    # Получаем все посты из базы данных
    posts = Post.query.all()
    # Получаем все пользователи из базы данных
    users = User.query.all()
    return render_template('home.html', users=users, posts=posts)
