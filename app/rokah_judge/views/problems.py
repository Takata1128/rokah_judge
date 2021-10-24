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
from werkzeug.utils import secure_filename
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


@problem.route("/upload_problem", methods=["POST"])
def upload_problem():
    if request.method == "POST":
        files = request.files.getlist("file")
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            register_problem(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("新しい問題が追加されました")
        return redirect(url_for("problem.show_problems"))


import zipfile


def register_problem(filepath):
    with zipfile.ZipFile(filepath) as zip:
        zip.extractall(app.config["UPLOAD_FOLDER"])
        pdir = os.path.splitext(filepath)[0]
        problem_dict = read_problem_file(pdir)
        cases = read_case_file(pdir, problem_dict["sample"])
        problem = Problem(
            problem_dict["title"],
            problem_dict["statement"],
            problem_dict["time"],
            problem_dict["memory"],
            problem_dict["constraints"],
            problem_dict["input"],
            problem_dict["output"],
            cases,
        )
        os.remove(filepath)
        db.session.add(problem)
        for case in cases:
            db.session.add(case)
        db.session.commit()


import re
import glob


def read_problem_file(dirpath):
    """ファイルを読み込み[title] などのタグによって問題情報を仕分け"""
    with open(os.path.join(dirpath, "problem")) as f:
        s = ""
        sample_list = []
        key = ""
        ret = DefaultDict()
        for line in f:
            m = re.match(r"\[(.+)\].*?", line)
            if m:
                if s != "":
                    ret[key] = s
                    s = ""
                key = m.group(1)
                continue
            else:
                if key == "sample":
                    sample_list.append(line)
                else:
                    s += line
        if key == "sample":
            ret[key] = sample_list
        elif s != "":
            ret[key] = s

        return ret


def read_case_file(dirpath, sample_list):
    """テストケースを読み込み"""
    ret = []
    in_files = glob.glob(os.path.join(dirpath, "in", "*"))
    for in_file in in_files:
        with open(in_file) as f:
            input_content = f.read()
        # 出力ファイル
        outfile_base = os.path.basename(os.path.splitext(in_file)[0]) + ".out"
        out_file = os.path.join(dirpath, "out", outfile_base)
        with open(out_file) as f:
            output_content = f.read()

        case = Testcase(
            os.path.basename(os.path.splitext(in_file)[0]),
            input_content,
            output_content,
            os.path.basename(in_file) in sample_list,
        )
        ret.append(case)
    return ret


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
