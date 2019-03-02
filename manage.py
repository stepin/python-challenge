#!/usr/bin/env python

import os

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from challenge import create_app
from challenge import db
from challenge.models import Base

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('APPNAME_ENV', 'dev')
app = create_app('challenge.settings.%sConfig' % env.capitalize())

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your SQLAlchemy models
    """

    Base.metadata.create_all(db.engine)


if __name__ == "__main__":
    manager.run()
