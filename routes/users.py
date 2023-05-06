from database.db import db
from flask import Blueprint, jsonify, request
from middlewares.auth import authVerify
from models.users import User

users = Blueprint('users', __name__)

@users.route('/<id>', methods=['GET'])
@authVerify('admin', 'super-admin')
def get_user(id):
    # get the user by id and active
    user = User.query.filter_by(id=id,active=True).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    print(user.id)
    return jsonify({'data': user.serialize()}), 200

@users.route('/all', methods=['GET'])
@authVerify('admin', 'super-admin')
def get_users():
    users = User.query.filter_by(active=True).all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify({'data': users}), 200

@users.route('/:id', methods=['PUT'])
@authVerify('admin', 'super-admin')
def update_user(id):
    data = request.get_json()
    user = User.query.filter_by(id=id)._and(User.active == True).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.name = data['name'] if 'name' in data else user.name
    user.lastName = data['lastName'] if 'lastName' in data else user.lastName
    user.secondLastName = data['secondLastName'] if 'secondLastName' in data else user.secondLastName
    user.email = data['email'] if 'email' in data else user.email
    user.password = data['password'] if 'password' in data else user.password
    user.role = data['role'] if 'role' in data else user.role
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'}), 200

@users.route('/:id', methods=['DELETE'])
@authVerify('admin', 'super-admin')
def delete_user(id):
    user = User.query.filter_by(id=id).and_(User.active == True).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.active = False # logical delete, too keep the inegrity of the database
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'}), 200

@users.route('/', methods=['POST'])
@authVerify('admin', 'super-admin')
def create_user():
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
