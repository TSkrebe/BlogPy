import os


from app import db, create_app
from app.models import User
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell

application = create_app(os.environ.get('FLASK_CONFIG') or 'testing')

migrate = Migrate(application, db)
manager = Manager(application)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=application, User=User, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

