from rokah_judge import db
from rokah_judge.models.languages import Language
from rokah_judge.utils.problem import register_problem
import os

problem_dir = './problems'

if __name__ == "__main__":
    db.session.add(Language(name="python3"))
    for f in os.listdir(problem_dir):
        if os.path.isdir(os.path.join(problem_dir, f)):
            register_problem(os.path.join(problem_dir, f), False)
    db.session.commit()
