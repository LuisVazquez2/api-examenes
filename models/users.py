from database.db import db


class User(db.Model):
    """
    User model class

    Class to create a user object and store it in the database using SQLAlchemy ORM and flask-migrate for migrations.
    Args:
        db (object): SQLAlchemy object imported from database.db

    Returns:
        object: User object
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    secondLastName = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.String(100), nullable=False, default="student"
    )  # user-student, admin-teacher, super-admin
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime, nullable=True, onupdate=db.func.current_timestamp()
    )

    def __init__(
        self, name, lastName, secondLastName, email, password, role="user", active=True
    ):
        self.name = name
        self.lastName = lastName
        self.secondLastName = secondLastName
        self.email = email
        self.password = password
        self.role = role

    def __init__(
        self,
        name,
        lastName,
        password,
        secondLastName=None,
        email=None,
        role="user",
        active=True,
    ):
        self.name = name
        self.lastName = lastName
        self.secondLastName = secondLastName
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return "<User %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.lastName,
            "secondLastName": self.secondLastName,
            "email": self.email,
            "password": self.password,
            "role": self.role,
        }
