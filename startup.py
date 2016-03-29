#!/usr/bin/env python3
import os
import getpass

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


@manager.command
def add_user():
    while True:
        username = input("Username: ")
        exists = User.query.filter_by(username=username).first()
        if exists:
            print("User with such name already exist.")
            continue
        password = getpass.getpass("Password: ")
        password2 = getpass.getpass("Repeat password: ")
        if password == password2:
            user = User(username, password)
            user.save()
            print("User {} created".format(username))
        else:
            print("Passwords do not match...")
            continue
        break


def make_shell_context():
    return dict(app=application, User=User, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

