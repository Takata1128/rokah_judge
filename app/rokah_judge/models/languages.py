from rokah_judge import db
from datetime import datetime


class Language(db.Model):
    __tablename__ = "languages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name=None):
        self.name = name
