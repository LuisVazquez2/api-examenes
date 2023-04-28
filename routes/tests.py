from flask import Blueprint, jsonify, request
from database.db import db
from models.tests import Test
from models.questions import Question

tests = Blueprint('tests', __name__)


@tests.route('/', methods=['GET'])
def get_tests():
    print("get_tests")
    test = Test("Test 1", "Test 1 description")
    db.session.add(test)
    db.session.commit()

    print(test.id)

    question = Question(test.id, "Question 1", "Answer 1")
    db.session.add(question)
    db.session.commit()

    return jsonify("message: 'Test created successfully!'"), 201
