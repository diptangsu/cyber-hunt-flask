from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import abort
from flask import session

from decorators import login_required_custom

from models.team import Team
from models.submission import Submission
from models.question import Question

import os


question_blueprint = Blueprint('question_blueprint', __name__)


def get_all_questions():
    all_questions = []
    # .filter('id', 'name', 'points')

    def inner():
        return all_questions

    return inner


get_all_questions = get_all_questions()


def get_team_score(team):
    return 0


def get_question_images_files_and_links(question_id):
    base_path = f'./questions/static/questionsdata/{question_id}/'
    images_path = os.path.join(base_path, 'images')
    files_path = os.path.join(base_path, 'files')
    links_path = os.path.join(base_path, 'links')

    question_images = None
    question_files = None
    question_links = None
    if os.path.exists(images_path):
        question_images = [
            {
                'path': os.path.join(f'questionsdata/{question_id}/images', image_name),
                'name': image_name
            }
            for image_name in os.listdir(images_path)
        ]
    if os.path.exists(files_path):
        question_files = [
            {
                'path': os.path.join(f'questionsdata/{question_id}/files', filename),
                'name': filename
            }
            for filename in os.listdir(files_path)
        ]
    if os.path.exists(links_path):
        question_links = [
            {
                'path': os.path.join(f'questionsdata/{question_id}/links', link_name),
                'name': link_name
            }
            for link_name in os.listdir(links_path)
            if link_name.endswith('.html')
        ]

    return question_images, question_files, question_links


@question_blueprint.route('/question/<int:question_id>')
@login_required_custom
def question(question_id):
    all_questions = get_all_questions()
    team = Team.get(id=session['team_id'])
    this_question = Question.get(id=question_id)
    if this_question is None:
        abort(404)

    if request.method == 'GET':
        question_images, question_files, question_links = get_question_images_files_and_links(question_id)

        score = get_team_score(team)

        questions_answered = set(
            Submission.objects.values_list('question__id', flat=True).filter(team=team)
        )

        return render_template('question.html', **{
            'team': team,
            'score': score,
            'question': this_question,
            'questions_answered': questions_answered,
            'files': question_files,
            'images': question_images,
            'links': question_links,
            'questions_list': all_questions
        })
    elif request.method == 'POST':
        answer = request.POST.get('answer')
        if answer:
            if answer == this_question.answer:
                try:
                    Submission.objects.get(team=team, question=this_question)
                    flash('You have already answered this question', 'warning')
                except Submission.DoesNotExist:
                    submission = Submission(team_id=team.id, question_id=this_question.id)
                    submission.save()

                    flash(f'Correct answer!! You get {this_question.points} points', 'success')
            else:
                flash('Wrong answer', 'danger')
        else:
            flash('Please submit and answer', 'danger')

        return redirect('question_blueprint.question', question_id)


@question_blueprint.route('/submissions')
def submissions():
    ...


@question_blueprint.route('/leaderboard')
def leaderboard():
    ...
