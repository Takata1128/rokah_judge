from flask import render_template
from rokah_judge.models.submissions import Submission
from flask_login.utils import login_required
from flask import Blueprint

submission = Blueprint("submission", __name__)


@submission.route("/submissions/")
@login_required
def show_submissions():
    submissions = Submission.query.order_by(Submission.id.desc()).all()
    return render_template("submissions/list.html", submissions=submissions)


@submission.route("/submissions/<int:id>")
@login_required
def show_submission(id):
    submission = Submission.query.get(id)
    return render_template("submissions/show.html", submission=submission)
