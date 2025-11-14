from routers.home.main_home import home_bpp
from routers.check.oauth.register import register_bpp
from routers.check.oauth.login import login_bpp
from routers.swagger_bp import swagger_bpp
from routers.check.oauth2.github import github_oauth_bp
from routers.check.oauth2.google import oauth_bpp

def register_blueprints(app):
    app.register_blueprint(home_bpp)
    app.register_blueprint(register_bpp)
    app.register_blueprint(login_bpp)
    app.register_blueprint(swagger_bpp)
    app.register_blueprint(github_oauth_bp)
    app.register_blueprint(oauth_bpp)