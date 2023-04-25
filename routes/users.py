from flask import Blueprint, jsonify , request
from database.db import db
from models.users import User

users = Blueprint('users', __name__)

@users.route('/', methods=['GET', 'POST'])
def index():
    data = request.get_json()
    if request.method == 'POST':
        user = User(data['name'], data['lastName'], data['secondLastName'], data['email'], data['password'])
        db.session.add(user)
        db.session.commit()
        #return a message and the user
        return jsonify({'message': 'User created successfully!', 'user': user.serialize()}), 201