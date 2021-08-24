from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("flask_blog.config")
db = SQLAlchemy(app)

from flask_blog.views.views import view

app.register_blueprint(view)

from flask_blog.views.problems import problem

app.register_blueprint(problem)

from flask_blog.views.submissions import submission

app.register_blueprint(submission)

from flask_blog.views.auth import auth

app.register_blueprint(auth)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from flask_blog.models.users import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))