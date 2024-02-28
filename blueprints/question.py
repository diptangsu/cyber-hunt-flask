from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import abort
from flask import session
from flask import url_for

from sqlalchemy.sql import func

from decorators import login_required_custom

from models.team import Team
from models.submission import Submission
from models.question import Question

import os


question_blueprint = Blueprint('question_blueprint', __name__)


def get_all_questions():
    all_questions = Question.query.filter_by(visible=True)
    return all_questions


def get_team_score(team):
    team_submissions = Submission.query.filter_by(team_id=team.id)
    score = sum(submission.question.points for submission in team_submissions)

    return score


def create_files_dict(path, question_id, file_type):
    if os.path.exists(path):
        return [
            {
                'path': f'questionsdata/{question_id}/{file_type}s/{filename}',
                'name': filename,
            }
            for filename in os.listdir(path)
        ]
    else:
        return []


def get_question_images_files_and_links(question_id):
    base_path = f'./static/questionsdata/{question_id}/'
    images_path = os.path.join(base_path, 'images')
    files_path = os.path.join(base_path, 'files')
    links_path = os.path.join(base_path, 'links')

    question_images = create_files_dict(images_path, question_id, 'image')
    question_files = create_files_dict(files_path, question_id, 'file')
    question_links = create_files_dict(links_path, question_id, 'link')

    return question_images, question_files, question_links


def get_answered_questions(team):
    return set(
        submission.question.id
        for submission in Submission.query.filter_by(team_id=team.id)
    )


@question_blueprint.route('/question/<int:question_id>', methods=['GET', 'POST'])
@login_required_custom
def question(question_id):
    all_questions = get_all_questions()
    team = Team.get(id=session['team_id'])
    this_question = Question.get(id=question_id)
    if this_question is None:
        abort(404)

    if request.method == 'GET':
        question_images, question_files, question_links = (
            get_question_images_files_and_links(question_id)
        )
        score = get_team_score(team)
        questions_answered = get_answered_questions(team)

        return render_template(
            'question.html',
            **{
                'team': team,
                'score': score,
                'question': this_question,
                'questions_answered': questions_answered,
                'files': question_files,
                'images': question_images,
                'links': question_links,
                'questions_list': all_questions,
            },
        )
    elif request.method == 'POST':
        answer = request.form.get('answer')
        if answer:
            if answer == this_question.answer:
                if (
                    Submission.get(team_id=team.id, question_id=this_question.id)
                    is not None
                ):
                    flash('You have already answered this question', 'warning')
                else:
                    submission = Submission(
                        team_id=team.id, question_id=this_question.id
                    )
                    submission.save()

                    flash(
                        f'Correct answer!! You get {this_question.points} points',
                        'success',
                    )
            else:
                flash('Wrong answer', 'danger')
        else:
            flash('Please submit and answer', 'danger')

        return redirect(url_for('question_blueprint.question', question_id=question_id))


@question_blueprint.route('/submissions')
def submissions():
    all_submissions = (
        Question.query.outerjoin(Submission)
        .group_by(Question.id)
        .order_by(Question.id)
        .with_entities(
            Question.id, Question.name, func.count(Submission.id).label('submissions')
        )
        .all()
    )

    return render_template('submissions.html', **{'submissions': all_submissions})


@question_blueprint.route('/leaderboard')
def leaderboard():
    team_scores = (
        Team.query.outerjoin(Submission)
        .outerjoin(Question)
        .group_by(Team.team_name)
        .with_entities(
            Team.team_name, func.coalesce(func.sum(Question.points), 0).label('score')
        )
        .with_labels()
        .all()
    )

    return render_template('leaderboard.html', **{'team_scores': team_scores})
