import re
import glob
import zipfile
import os
from typing import DefaultDict
from flask_login.utils import login_required
from flask import request, redirect, url_for, render_template, flash, session
from rokah_judge.models.testcases import Testcase
from rokah_judge import db, app
from rokah_judge.utils.message import push
from rokah_judge.models.problems import Problem
from rokah_judge.models.submissions import Submission
from rokah_judge.models.languages import Language
from rokah_judge.utils.problem import unzip_problem, register_problem
from werkzeug.utils import secure_filename
from flask import Blueprint

problem = Blueprint("problem", __name__)


@problem.route("/problems/<int:id>", methods=["GET"])
@login_required
def show_problem(id):
    problem = Problem.query.get(id)
    samples = Testcase.query.filter(
        Testcase.problem_id == id, Testcase.is_sample).order_by(Testcase.id.desc()).all()
    languages = Language.query.order_by(Language.id.desc()).all()
    return render_template("problems/show.html", problem=problem, samples=samples, languages=languages)


@problem.route("/problems/", methods=["GET"])
@login_required
def show_problems():
    problems = Problem.query.order_by(Problem.id.desc()).all()
    return render_template("problems/list.html", problems=problems)


@problem.route("/problems/new", methods=["GET"])
@login_required
def new_problem():
    return render_template("problems/new.html")


@problem.route("/upload_problem", methods=["POST"])
def upload_problem():
    if request.method == "POST":
        files = request.files.getlist("file")
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            pdir = unzip_problem(os.path.join(
                app.config["UPLOAD_FOLDER"], filename))
            register_problem(pdir)
        flash("新しい問題が追加されました")
        return redirect(url_for("problem.show_problems"))


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
    cases = Testcase.query.filter(
        Testcase.problem_id == id).order_by(Testcase.id.desc()).all()
    return render_template("problems/edit.html", problem=problem, cases=cases)


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

    case_indices = request.form.getlist("testcase_index[]")
    case_inputs = request.form.getlist("testcase_input[]")
    case_outputs = request.form.getlist("testcase_output[]")
    is_samples = request.form.getlist("is_sample")

    for id, input, output, is_sample in zip(case_indices, case_inputs, case_outputs, is_samples):
        if id == -1:
            case = Testcase("edit", input, output, is_sample)
        else:
            case = Testcase.query.get(id)
            case.input = input
            case.output = output
            case.is_sample = True if is_sample == '1' else False
            print(id)
            print(input)
            print(output)
            print(is_sample)
        db.session.merge(case)
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
