from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from rokah_judge import app
from functools import wraps

view = Blueprint("view", __name__)


@view.route("/", methods=["GET"])
def top():
    return render_template("top.html")
