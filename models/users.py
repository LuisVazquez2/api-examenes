from database.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=True)
    secondLastName = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=True)
    # role = db.Column(db.String(100), nullable=False)
    # status = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True,
                           onupdate=db.func.current_timestamp())
    # deleted_at = db.Column(db.DateTime, nullable=False)

    # def init method with properties optional
    def __init__(self, name, lastName, secondLastName, email, password):
        self.name = name
        self.lastName = lastName
        self.secondLastName = secondLastName
        self.email = email
        self.password = password
        # self.role = role
        # self.status = status
        self.created_at = db.func.current_timestamp()
        # self.updated_at = updated_at
        # self.deleted_at = deleted_at

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastName': self.lastName,
            'secondLastName': self.secondLastName,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at,
        }

    def serialize_with_token(self, token):
        return {
            'id': self.id,
            'name': self.name,
            'lastName': self.lastName,
            'secondLastName': self.secondLastName,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at,
            'token': token
        }
