from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("rokah_judge.config")
db = SQLAlchemy(app)

from rokah_judge.views.views import view

app.register_blueprint(view)

from rokah_judge.views.problems import problem

app.register_blueprint(problem)

from rokah_judge.views.submissions import submission

app.register_blueprint(submission)

from rokah_judge.views.auth import auth

app.register_blueprint(auth)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from rokah_judge.models.users import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))