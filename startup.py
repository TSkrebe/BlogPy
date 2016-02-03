#!/usr/bin/env python3
import os


from app import db, create_app
from app.models import User
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell
from markdown import markdown

application = create_app(os.environ.get('FLASK_CONFIG') or 'testing')

migrate = Migrate(application, db)
manager = Manager(application)
manager.add_command('db', MigrateCommand)


@application.template_filter("markdown")
def markdown_filter(code):
    return markdown(code, extensions=['codehilite', 'fenced_code'])


def make_shell_context():
    return dict(app=application, User=User, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

