from functools import wraps
from flask import request, jsonify
from utils.auth import verifyHeader, verifyToken, getPayloadFromToken


def authVerify(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            header = verifyHeader(request)
            if header is None:
                return jsonify({"message": "Token does not provided"}), 401

            token = verifyToken(header) # if the token is not valid, verifyToken returns False else returns the payload

            if type(token) == bool and not token:
                return jsonify({"message": "Invalid token"}), 401

            currentUserRole = token["role"]  # get the role from the token

            # if the role of the user is not in the list of roles authorized to access the resource, return 403
            if currentUserRole not in roles:
                return (
                    jsonify(
                        {
                            "mensaje": "You do not have permission to access this resource"
                        }
                    ),
                    403,
                )

            # if the user has permission, continue with the request

            return f(*args, **kwargs)

        return wrapped

    return wrapper
