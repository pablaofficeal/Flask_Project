from routers.home.main_home import home_bpp
from routers.check.oauth.register import register_bpp
from routers.check.oauth.login import login_bpp
from routers.swagger_bp import swagger_bpp
from routers.check.oauth2.github import github_oauth_bp
from routers.check.oauth2.google import oauth_bpp
from api.create_post_api import cpa_bpp
from routers.home.home import homes_bpp
from routers.home.profile import profile_bpp
from api.delete_post_api import dpa_bpp
from api.edit_post_api import epa_bpp
from routers.check.oauth.logout import logout_bpp



def register_blueprints(app):
    app.register_blueprint(home_bpp)
    app.register_blueprint(register_bpp)
    app.register_blueprint(login_bpp)
    app.register_blueprint(swagger_bpp)
    app.register_blueprint(github_oauth_bp)
    app.register_blueprint(oauth_bpp)
    app.register_blueprint(cpa_bpp)
    app.register_blueprint(homes_bpp)
    app.register_blueprint(profile_bpp)
    app.register_blueprint(dpa_bpp)
    app.register_blueprint(epa_bpp)
    app.register_blueprint(logout_bpp)