from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from flask_blog import app
from functools import wraps

view = Blueprint("view", __name__)


def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("view.login"))
        return view(*args, **kwargs)

    return inner


@view.route("/", methods=["GET"])
def top():
    return render_template("top.html")


@view.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            flash("ユーザ名が異なります")
        elif request.form["password"] != app.config["PASSWORD"]:
            flash("パスワードが異なります")
        else:
            session["logged_in"] = True
            flash("ログインしました")
            return redirect(url_for("view.top"))
    return render_template("login.html")


@view.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("ログアウトしました")
    return redirect(url_for("view.top"))


@view.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for("view.login"))
