from rokah_judge import db
from rokah_judge.models.languages import Language

if __name__ == "__main__":
    db.session.add(Language(name="python3"))
    db.session.commit()
