from flask_login.utils import login_required
from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import db
from flask_blog.utils.message import push
from flask_blog.models.problems import Language, Problem, Submission
from flask import Blueprint

problem = Blueprint("problem", __name__)


@problem.route("/problems/<int:id>", methods=["GET"])
@login_required
def show_problem(id):
    problem = Problem.query.get(id)
    languages = Language.query.order_by(Language.id.desc()).all()
    return render_template("problems/show.html", problem=problem, languages=languages)


@problem.route("/problems/", methods=["GET"])
@login_required
def show_problems():
    problems = Problem.query.order_by(Problem.id.desc()).all()
    return render_template("problems/list.html", problems=problems)


@problem.route("/problems/new", methods=["GET"])
@login_required
def new_problem():
    return render_template("problems/new.html")


@problem.route("/problems/add", methods=["POST"])
@login_required
def add_problem():
    problem = Problem(
        title=request.form["title"],
        text=request.form["text"],
        time_limit=request.form["time_limit"],
        memory_limit=request.form["memory_limit"],
        constraint=request.form["constraint"],
        input=request.form["input"],
        output=request.form["output"],
    )
    db.session.add(problem)
    db.session.commit()
    flash("新しい問題が作成されました")
    return redirect(url_for("problem.show_problems"))


@problem.route("/problems/<int:id>/edit", methods=["GET"])
@login_required
def edit_problem(id):
    problem = Problem.query.get(id)
    return render_template("problems/edit.html", problem=problem)


@problem.route("/problems/<int:id>/update", methods=["POST"])
@login_required
def update_problem(id):
    problem = Problem.query.get(id)
    problem.title = request.form["title"]
    problem.text = request.form["text"]
    problem.time_limit = request.form["time_limit"]
    problem.memory_limit = request.form["memory_limit"]
    problem.constraint = request.form["constraint"]
    problem.input = request.form["input"]
    problem.output = request.form["output"]
    db.session.merge(problem)
    db.session.commit()
    flash("問題が更新されました")
    return redirect(url_for("problem.show_problems"))


@problem.route("/problems/<int:id>/delete", methods=["POST"])
@login_required
def delete_problem(id):
    problem = Problem.query.get(id)
    db.session.delete(problem)
    db.session.commit()
    flash("記事が削除されました")
    return redirect(url_for("problem.show_problems"))


@problem.route("/problems/<int:id>/submit", methods=["POST"])
@login_required
def submit(id):
    submission = Submission(
        problem_id=id,
        language=request.form["language"],
        code=request.form["code"],
        status="WJ",
        ac=0,
        wa=0,
        tle=0,
        re=0,
    )
    db.session.add(submission)
    db.session.commit()
    push(id=submission.id)
    flash("解答が提出されました")
    return redirect(url_for("submission.show_submissions"))
