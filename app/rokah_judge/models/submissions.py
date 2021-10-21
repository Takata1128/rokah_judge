from rokah_judge import db
from datetime import datetime


class Submission(db.Model):
    __tablename__ = "submissions"
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
        self.submitted_at = datetime.utcnow()
