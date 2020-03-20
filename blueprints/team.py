from flask import Blueprint


team_blueprint = Blueprint('team', __name__)


@team_blueprint.route('/')
def index():
    return 'Hello World'
