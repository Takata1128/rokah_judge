from flask_blog import db
from datetime import datetime


class Problem(db.Model):
    __tablename__ = "problems"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    text = db.Column(db.Text)
    time_limit = db.Column(db.Integer)
    memory_limit = db.Column(db.Integer)
    constraint = db.Column(db.Text)
    input = db.Column(db.Text)
    output = db.Column(db.Text)
    sample = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    def __init__(
        self,
        title=None,
        text=None,
        time_limit=None,
        memory_limit=None,
        constraint=None,
        input=None,
        output=None,
        sample=None,
    ):
        self.title = title
        self.text = text
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.constraint = constraint
        self.input = input
        self.output = output
        self.sample = sample
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return "<Entry id:{} title:{} text:{} time_limit:{} memory_limit:{} constraint:{} input:{} output:{} sample:{}".format(
            self.id,
            self.title,
            self.text,
            self.time_limit,
            self.memory_limit,
            self.constraint,
            self.input,
            self.output,
            self.sample,
        )


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    problem_id = db.Column(db.Integer)
    language = db.Column(db.String(20))
    code = db.Column(db.Text)
    status = db.Column(db.String(20))
    ac = db.Column(db.Integer)
    wa = db.Column(db.Integer)
    tle = db.Column(db.Integer)
    re = db.Column(db.Integer)
    submitted_at = db.Column(db.DateTime)

    def __init__(
        self,
        user_id=None,
        problem_id=None,
        language=None,
        code=None,
        status=None,
        ac=None,
        wa=None,
        tle=None,
        re=None,
    ):
        self.user_id = user_id
        self.problem_id = problem_id
        self.language = language
        self.code = code
        self.status = status
        self.ac = ac
        self.wa = wa
        self.tle = tle
        self.re = re


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name=None):
        self.name = name
