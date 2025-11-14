from flask import Blueprint, jsonify, render_template, current_app
import json
import sys
import os

# Добавляем путь к utils в sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.swagger_generator import create_swagger_spec, auto_swagger

swagger_bpp = Blueprint('swagger_bpp', __name__, url_prefix='/api')

@swagger_bpp.route('/swagger.json')
def swagger_json():
    try:
        from flask import current_app
        spec = create_swagger_spec(current_app)
        return jsonify(spec)
    except Exception as e:
        import traceback
        return jsonify({
            "error": f"Ошибка генерации спецификации: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@swagger_bpp.route('/docs')
def swagger_ui():
    return render_template('swagger.html')