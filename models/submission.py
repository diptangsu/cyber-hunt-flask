from db import db
import datetime
from .team import Team
from .question import Question


class Submission(db.Model):
    __tablename__ = 'Submissions'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey(Team.id))
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))
    timestamp = db.Column(db.DateTime(), default=datetime.datetime.now)

    team = db.relationship('Team')
    question = db.relationship('Question')

    def __init__(self, team_id, question_id):
        self.team_id = team_id
        self.question_id = question_id

    def __repr__(self):
        return f'({self.timestamp.strftime("%d/%m %H:%M")}): {self.team} -> {self.question}'
