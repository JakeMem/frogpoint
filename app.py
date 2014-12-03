from flask import Flask, g
from flask_login import LoginManager, current_user

from parse_rest.connection import register

from models.merchant import Merchant
from routes.dashboard import dashboard
from routes.auth import auth


app = Flask(__name__)
app.config.from_object(__package__ + '.default_settings')
try:
    app.config.from_object(__package__ + '.local_settings')
except ImportError:
    pass

app.register_blueprint(auth)
app.register_blueprint(dashboard)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = ''
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    if userid:
        return Merchant.by_id(userid)


@app.before_request
def app_globals():
    register(app.config['PARSE_APPLICATION_ID'],
             app.config['PARSE_REST_API_KEY'])
    g.user = current_user
