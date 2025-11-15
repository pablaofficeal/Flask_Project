from flask import Blueprint, request, jsonify, current_app, url_for
from models.main_rou_imp_db import *
from models.imp import db

cpa_bpp = Blueprint('cpa_bpp', __name__)

@cpa_bpp.route('/create_post', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')

    if not title or not content or not user_id:
        return jsonify({'error': 'Missing required fields'}), 400

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully', 'post_id': new_post.id}), 201