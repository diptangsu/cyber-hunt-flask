from flask import Blueprint


team_blueprint = Blueprint('team_blueprint', __name__)


@team_blueprint.route('/register')
def register():
    ...


@team_blueprint.route('/login')
def login():
    ...


@team_blueprint.route('/logout')
def logout():
    ...
