from flask import Blueprint, render_template, request, redirect, url_for, session
from api.create_post_api import create_post
from models.main_rou_imp_db import Post
from models.imp import db

create_post_bpp = Blueprint('create_post_bpp', __name__)

@create_post_bpp.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home.home'))
    return render_template('create-post.html')