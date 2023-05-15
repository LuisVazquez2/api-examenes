from database.db import db
from flask import Blueprint, jsonify, request
from middlewares.auth import authVerify
from models.users import User

users = Blueprint("users", __name__)


@users.route("/<id>", methods=["GET"])
@authVerify("admin", "super-admin")
def get_user(id: int):
    """
    get_user is a function that returns a user by id


    Args:
        id (int): id of the user

    Returns:
        object: User object serialized in JSON
    """
    # get the user by id and active
    user = User.query.filter_by(id=id, active=True).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    print(user.id)
    return jsonify({"data": user.serialize()}), 200


@users.route("/", methods=["GET"])
@authVerify("admin", "super-admin")
def get_users():
    """
    get_users is a function that returns all users active

    Get all users active in the database with pagination (!pending)

    Returns:
        object: Users object serialized in JSON
    """

    # TODO: pagination
    users = User.query.filter_by(active=True).all()

    if not users:
        return jsonify({"message": "Users not found"}), 404

    users = list(map(lambda user: user.serialize(), users))
    return jsonify({"data": users}), 200


@users.route("/<id>", methods=["PUT"])
@authVerify("admin", "super-admin")
def update_user(id: int):
    """
    update_user is a function that updates a user by id

    Given an id, the function updates the user with the data sent in the request

    Args:
        id (int): id of the user

    Returns:
        object: message of the result of the update
    """
    # get the data from the request
    data = request.get_json()

    user = User.query.filter_by(id=id, active=True).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.name = data["name"] if "name" in data else user.name

    user.lastName = data["lastName"] if "lastName" in data else user.lastName

    user.secondLastName = (
        data["secondLastName"] if "secondLastName" in data else user.secondLastName
    )

    user.email = data["email"] if "email" in data else user.email

    user.password = data["password"] if "password" in data else user.password

    user.role = data["role"] if "role" in data else user.role

    db.session.commit()

    # TODO: optimize the process of update user using the function update from sqlalchemy or add validation of the payload sent by the client

    return jsonify({"message": "User updated successfully!"}), 200


@users.route("/<id>", methods=["DELETE"])
@authVerify("admin", "super-admin")
def delete_user(id: int):
    """
    delete_user is a function that deletes a user by id

    The function logical deletes the user by id, changing the active field to False to keep the integrity of the information in the database

    Args:
        id (int): id of the user

    Returns:
        object: message of the result of the delete
    """
    user = User.query.filter_by(id=id, active=True).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.active = False # logical delete

    db.session.commit()

    return jsonify({"message": "User deleted successfully!"}), 200


@users.route("/", methods=["POST"])
@authVerify("admin", "super-admin")
def create_user():
    """
    create_user is a function that creates a user

    Given a payload, the function creates a user in the database

    Returns:
        object: message of the result of the create and the id of the user created
    """
    data = request.get_json()
    # validate the duplicated email
    user = User.query.filter_by(email=data["email"]).first()
    if user:
        return jsonify({"message": "The email already exists"}), 409

    # create the user
    user = User(
        name=data["name"] if "name" in data else None,
        lastName=data["lastName"] if "lastName" in data else None,
        secondLastName=data["secondLastName"] if "secondLastName" in data else None,
        email=data["email"] if "email" in data else None,
        password=data["password"] if "password" in data else None,
        role=data["role"] if "role" in data else None,
    )
    db.session.add(user)
    db.session.commit()
    # return a message and the user
    return (
        jsonify(
            {
                "message": "User created successfully!",
                "data": {
                    "id": user.id,
                },
            }
        ),
        201,
    )
