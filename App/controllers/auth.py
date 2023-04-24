from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.database import db
from App.models import *
from App.controllers import *


def jwt_authenticate(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None

def signup_user(first_name, last_name, email, username, password):
    newuser = create_user(first_name, last_name, email, username, password)
    return newuser


def signup_coordinator(first_name, last_name, email, username, password, organization_name): 
    newcoordinator = create_coordinator(first_name, last_name, email, username, password, organization_name)
    return newcoordinator


def login_competitor(username, password):
    user = RegularUser.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


def login_coordinator(username, password):
    coordinator = Coordinator.query.filter_by(username = username).first()
    if coordinator and coordinator.check_password(password):
        return coordinator
    return None


def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    return login_manager


def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt