from flask import request, redirect, url_for, render_template, flash, session, Blueprint
from flask_login.utils import login_required, login_user, logout_user
from flask_blog import db
from flask_blog.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your email or password and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("view.top"))


@auth.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()

    if user:  # already exists
        flash("すでに使用されているメールアドレスです！")
        return redirect(url_for("auth.signup"))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
    )

    db.session.add(new_user)
    db.session.commit()
    flash("ユーザー登録が完了しました！")
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました")
    return redirect(url_for("view.top"))


@auth.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for("auth.login"))
