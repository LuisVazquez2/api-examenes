from flask import Blueprint
from routes.users import users
from routes.tests import tests

router = Blueprint('router', url_prefix='/api', import_name=__name__)

router.register_blueprint(tests, url_prefix='/tests')
router.register_blueprint(users, url_prefix='/users')