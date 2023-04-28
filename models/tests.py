from database.db import db


class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True,
                           onupdate=db.func.current_timestamp())

    def __init__(self, name, description, active=True):
        self.name = name
        self.description = description
        self.active = active


    def __repr__(self):
        return '<Test %r>' % self.name

    def get_absolute_url(self):
        return reverse("Test_detail", kwargs={"pk": self.pk})

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }
        