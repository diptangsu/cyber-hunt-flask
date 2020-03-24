from flask import Blueprint
from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request


question_blueprint = Blueprint('question_blueprint', __name__)


@question_blueprint.route('/question/<int:question_id>')
def question(question_id):
    ...


@question_blueprint.route('/submissions')
def submissions():
    ...


@question_blueprint.route('/leaderboard')
def leaderboard():
    ...
