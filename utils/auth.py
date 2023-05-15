import os
import jwt
import bcrypt
from datetime import datetime, timedelta


def hashPassword(password):
    """
    hashPassword function is used to encrypt the user's password.

    The function uses the bycrypt library to encrypt the password.

    Args:
        password (string): Password to be encrypted.

    Returns:
        string: If the password is encrypted correctly, it returns the encrypted password. If the password is not encrypted correctly, it returns None.
    """
    try:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    except:
        return None


def verifyPassword(password, hash):
    """
    verifyPassword function is used to verify that the password sent by the user is the same as the one stored in the database.

    The function uses the bycrypt library to verify that the password sent by the user is the same as the one stored in the database.

    Args:
        password (string): Password sent by the user.
        hash (string): Password stored in the database.

    Returns:
        boolean: If the password is the same, it returns True. If the password is not the same, it returns False.
    """
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hash)
    except:
        return False


def verifyHeader(req):
    """
    verifyHeader function is used to verify that the request header contains the Authorization field.

    Checks that the Authorization field is not empty and that it contains the word Bearer.

    Args:
        req (request): Request object sent by the user.

    Returns:
        string: Token sent by the user in the request header. If the token is not found, it returns None.
    """
    if "Authorization" not in req.headers:
        return None

    authHeader = req.headers["Authorization"]

    if authHeader == "":
        return None

    authHeader = authHeader.split(" ") # split the header by space

    if len(authHeader) != 2:
        return None

    if authHeader[0] != "Bearer":
        return None

    return authHeader[1]


def verifyToken(token):
    """
    verifyToken function is used to verify the token sent by the user in the request header.

    The function uses the jwt library to decode the token and verify that it is valid.

    Args:
        token (string): Token sent by the user in the request header.

    Returns:
        dict: If the token is valid, it returns the payload of the token. If the token is invalid, it returns False.
    """

    try:
        response = jwt.decode(
            token,
            os.environ.get("JWT_SECRET"),
            algorithms=os.getenv("JWT_ALGORITHM"),
            options={"verify_exp": True},
        )
        id = response["id"]
        # TODO: verify if the user exists in the database, if not, return False
        return response
    except:
        return False


def signToken(payload, expiration=True):
    """
    signToken function is used to generate a token.

    The function uses the jwt library to generate a token with the payload sent by the user.

    If in the payload does not exist the field 'role', the function will add the field 'role' with the value 'student'.

    Args:
        payload (dict): Payload to be included in the token.
        expiration (bool, optional): Indicates if the token will have an expiration date. Defaults to True.

    Returns:
        string: If the token is generated correctly, it returns the token. If the token is not generated correctly, it returns False.
    """
    try:
        if expiration:
            payload["exp"] = datetime.utcnow() + timedelta(
                hours=float(os.getenv("LIFE_TOKEN_HOURS"))
            )

        payload["iat"] = datetime.utcnow()

        if not "role" in payload:
            payload["role"] = "student"

        return jwt.encode(
            payload, os.environ.get("JWT_SECRET"), algorithm=os.getenv("JWT_ALGORITHM")
        )
    except:
        return False


def getPayloadFromToken(token):
    """
    getPayloadFromToken function is used to extract the payload from a token.

    The function uses the jwt library to decode the token and extract the payload.
    ¡¡Attention: This function does not verify that the token is valid.!!

    Args:
        token (string): Token sent by the user in the request header.

    Returns:
        dict: If the token is valid, it returns the payload of the token. If the token is invalid, it returns False.
    """
    try:
        return jwt.decode(
            token,
            os.environ.get("JWT_SECRET"),
            algorithms=os.getenv("JWT_ALGORITHM"),
        )
    except:
        return False


def getIdFromToken(token):
    """
    getIdFromToken function is used to extract the id from a token.

    The function uses the jwt library to decode the token and extract the id.

    Args:
        token (string): Token sent by the user in the request header.

    Returns:
        string: If the token is valid, it returns the id of the token. If the token is invalid, it returns None.
    """
    payload = getPayloadFromToken(token)
    try:
        if payload:
            return payload["id"]
        else:
            return None
    except:
        return None
