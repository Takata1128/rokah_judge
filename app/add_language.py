from flask_blog import db
from flask_blog.models.problems import Language

if __name__ == '__main__':
    db.session.add(Language(name='cpp'))
    db.session.add(Language(name='python3'))
    db.session.commit()
    