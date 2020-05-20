if __name__ == "__main__":
	from dotenv import load_dotenv
	from pathlib import Path
	env_path = Path('.') / '.env'
	load_dotenv(dotenv_path=env_path)


import os, atexit
from flask import Flask, escape, request, json
from flask_cors import CORS
from utils.dbConf import db, write_connection_string
from utils.basicFolder import create_folders

# print("write_connection_string: ", write_connection_string)


app = Flask(__name__)
CORS(app)

app.debug = os.getenv("DEBUG") if os.getenv("DEBUG") else True

app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

create_folders()

@app.route('/')
def hello():
	name = request.args.get("name", "World")
	return f'Hello, {escape(name)}!'


try:
	from src.routes import routes
	for route in routes:
		app.register_blueprint(route[1], url_prefix=route[0])
	from utils.schedulers import cron
	atexit.register(lambda: cron.shutdown(wait=False))
except Exception as e:
	print("Error: ",e)


if __name__ == '__main__':
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = write_connection_string
	db.init_app(app)
	app.run()
