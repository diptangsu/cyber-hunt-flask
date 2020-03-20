from flask_admin.contrib.sqla import ModelView
from db import db
from models.team import Team
from models.question import Question
from models.submission import Submission


def add_admin_views(admin):
    admin.add_view(ModelView(Team, db.session))
    admin.add_view(ModelView(Question, db.session))
    admin.add_view(ModelView(Submission, db.session))
