from rokah_judge import db


class Testcase(db.Model):
    __tablename__ = "testcases"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    is_sample = db.Column(db.Boolean)
    content = db.Column(db.Text)
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), nullable=False)
