from flask import Blueprint, request, jsonify
from models.main_rou_imp_db import Post
from models.imp import db

epa_bpp = Blueprint('epa_bpp', __name__)

@epa_bpp.route('/edit_post', methods=['PUT'])
def edit_post():
    data = request.get_json()
    post_id = data.get('post_id')
    title = data.get('title')
    content = data.get('content')

    if not post_id:
        return jsonify({'error': 'Post ID is required'}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    if title:
        post.title = title
    if content:
        post.content = content

    db.session.commit()

    return jsonify({'message': 'Post updated successfully'}), 200
