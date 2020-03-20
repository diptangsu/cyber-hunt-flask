from flask import Flask
from flask_admin import Admin

from admin import add_admin_views
from blueprints.question import question_blueprint
from blueprints.team import team_blueprint


app = Flask(__name__)
app.config.from_pyfile('config.py')

admin = Admin(app, name='cyberhunt', template_mode='bootstrap3')
add_admin_views(admin)

app.register_blueprint(question_blueprint)
app.register_blueprint(team_blueprint)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return 'Working'


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0')
