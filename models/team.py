from db import db


class Team(db.Model):
    __tablename__ = 'Teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, team_name, email, phone, password):
        self.team_name = team_name
        self.email = email
        self.phone = phone
        self.password = password

    def __repr__(self):
        return f'{self.team_name}'
