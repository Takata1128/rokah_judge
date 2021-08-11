from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
