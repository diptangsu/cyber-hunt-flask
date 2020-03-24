from flask import Blueprint


question_blueprint = Blueprint('question_blueprint', __name__)


@question_blueprint.route('/<int:question_id>')
def question(question_id):
    ...


@question_blueprint.route('/submissions')
def submissions():
    ...


@question_blueprint.route('/leaderboard')
def leaderboard():
    ...
