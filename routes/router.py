from flask import Blueprint
from routes.users import users

router = Blueprint('router', __name__)

router.register_blueprint(users, url_prefix='/users')
