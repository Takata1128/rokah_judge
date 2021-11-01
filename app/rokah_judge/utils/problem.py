from rokah_judge import db, app
import zipfile
import os
from typing import DefaultDict
import re
import glob
from rokah_judge.models.problems import Problem
from rokah_judge.models.testcases import Testcase


def unzip_problem(filepath):
    with zipfile.ZipFile(filepath) as zip:
        zip.extractall(app.config["UPLOAD_FOLDER"])
    pdir = os.path.splitext(filepath)[0]
    return pdir


def register_problem(filepath, remove=True):
    problem_dict = read_problem_file(filepath)
    cases = read_case_file(filepath, problem_dict["sample"])
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
    if remove:
        os.remove(filepath)
    db.session.add(problem)
    for case in cases:
        db.session.add(case)
    db.session.commit()


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
