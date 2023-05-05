from database.db import db


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_id = db.Column(db.Integer, db.ForeignKey("tests.id"), nullable=False)
    question = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime, nullable=True, onupdate=db.func.current_timestamp()
    )

    def __init__(self, test_id, question, answer, active=True):
        self.test_id = test_id
        self.question = question
        self.answer = answer
        self.active = active

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Question_detail", kwargs={"pk": self.pk})
