from flask import Blueprint, request, jsonify
from models.main_rou_imp_db import Post
from models.imp import db

dpa_bpp = Blueprint('dpa_bpp', __name__)


@dpa_bpp.route('/delete_post', methods=['DELETE'])
def delete_post():
    data = request.get_json()
    post_id = data.get('post_id')

    if not post_id:
        return jsonify({'error': 'Post ID is required'}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully'}), 200