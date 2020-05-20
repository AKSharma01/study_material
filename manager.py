from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from model import *
from utils.dbConf import db, write_connection_string
from server import app


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = write_connection_string
db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


####macos
# brew uninstall vapor
# brew install vapor/tap/vapor
###linux
# sudo apt-get build-essential python-dev

if __name__ == '__main__':
	manager.run()