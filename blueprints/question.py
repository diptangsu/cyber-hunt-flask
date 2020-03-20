from flask import Blueprint


question_blueprint = Blueprint('question', __name__)


@question_blueprint.route('/')
def index():
    return 'Hello World'
