from flask_blog import app, db
from flask_migrate import Migrate

db.init_app(app)
Migrate(app, db)

if __name__ == "__main__":
    app.run()
