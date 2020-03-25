from flask import Blueprint
from flask import flash
from flask import session
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from models.team import Team
from decorators import login_required_custom

team_blueprint = Blueprint('team_blueprint', __name__)


@team_blueprint.route('/')
def index():
    return redirect(url_for('team_blueprint.login'))


@team_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """
    GET /register -> return the register page
    POST /register -> register user and redirect to login
    """
    if request.method == 'GET':
        return render_template('register.html')
    else:
        team_name = request.form.get('teamname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if all((team_name, phone, email, password, password2)):
            if password == password2:
                team = Team(team_name=team_name, phone=phone, email=email, password=password)
                team.save()

                flash('New team added successfully', 'success')
                return redirect(url_for('question_blueprint.question', question_id=1))
            else:
                flash('Passwords don\'t match', 'danger')
                return render_template('register.html')
        else:
            flash('All fields are required', 'danger')
            return render_template('register.html')


@team_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'team_id' in session:
        flash('You are already logged in', 'info')
        return redirect(url_for('question_blueprint.question', question_id=1))
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('teamname')
        password = request.form.get('password')

        if email and password:
            team = Team.get(email=email, password=password)
            if team is None:
                flash('Team name or password incorrect', 'danger')
                return render_template('login.html')

            session['team_id'] = team.id
            return redirect(url_for('question_blueprint.question', question_id=1))
        else:
            flash('Team name or password fields are required', 'danger')
            return render_template('login.html')


@team_blueprint.route('/logout')
@login_required_custom
def logout():
    del session['team_id']
    return redirect(url_for('question_blueprint.login'))
