from flask_blog.views.views import login_required
from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import db
from flask_blog.utils.message import push
from flask_blog.models.problems import Language, Problem, Submission
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
