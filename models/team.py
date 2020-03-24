from db import db


class Team(db.Model):
    __tablename__ = 'Teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, team_name, phone, email, password):
        self.team_name = team_name
        self.phone = phone
        self.email = email
        self.password = password

    def __repr__(self):
        return f'{self.team_name}'

    @classmethod
    def get(cls, **kwargs):
        if kwargs:
            return cls.query.filter_by(**kwargs).first()
        else:
            return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
