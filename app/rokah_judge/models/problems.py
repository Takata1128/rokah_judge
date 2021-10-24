from rokah_judge import db
from datetime import datetime
from rokah_judge.models.testcases import Testcase


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
    created_at = db.Column(db.DateTime)
    cases = db.relationship("Testcase", backref="problem", lazy=False)

    def __init__(
        self,
        title=None,
        text=None,
        time_limit=None,
        memory_limit=None,
        constraint=None,
        input=None,
        output=None,
        cases=None,
    ):
        self.title = title
        self.text = text
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.constraint = constraint
        self.input = input
        self.output = output
        self.cases = cases
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
