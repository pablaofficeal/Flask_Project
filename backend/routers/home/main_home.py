from flask import Blueprint, render_template

home_bpp = Blueprint('home_bpp', __name__)

@home_bpp.route('/')
def index():
    return render_template('index.html')