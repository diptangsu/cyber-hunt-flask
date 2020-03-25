from db import db


class Question(db.Model):
    __tablename__ = 'Questions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    body = db.Column(db.Text())
    hint = db.Column(db.String(200))
    answer = db.Column(db.String(100))
    points = db.Column(db.Integer())
    visible = db.Column(db.Boolean())

    def __init__(self, name, body, hint, answer, points, visible):
        self.name = name
        self.body = body
        self.hint = hint
        self.answer = answer
        self.points = points
        self.visible = visible

    def __repr__(self):
        return f'{self.id}. {self.name} [{self.points}]'

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
