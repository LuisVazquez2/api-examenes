from flask import Blueprint, jsonify, request
from database.db import db
from models.users import User

users = Blueprint('users', __name__)


@users.route('/', methods=['POST'])
def index():
    data = request.get_json()

    # validate the duplicated email
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'message': 'The email already exists'}), 409

    # create the user
    user = User(
        name=data['name'] if 'name' in data else None,
        lastName=data['lastName'] if 'lastName' in data else None,
        secondLastName=data['secondLastName'] if 'secondLastName' in data else None,
        email=data['email'] if 'email' in data else None,
        password=data['password'] if 'password' in data else None,
        role=data['role'] if 'role' in data else None,
    )
    db.session.add(user)
    db.session.commit()
    # return a message and the user
    return jsonify({'message': 'User created successfully!',
                    'data': {
                        'id': user.id,
                    }
                    }), 201
