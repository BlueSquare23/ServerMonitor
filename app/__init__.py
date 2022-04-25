from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

# Returns the main app.
def run_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = "AllYourBaseAreBelongToUs"
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	
	from .models import Host, Log, Alert, Outage
	create_database(app)
	
	# Pull in our main index route (aka home page)
	from app.index import index
	app.register_blueprint(index, url_prefix="/")
	
	# Pull in add_host route.
	from .add_host import add_host_blueprint
	app.register_blueprint(add_host_blueprint, url_prefix="/add_host")
	
	# Pull in all_logs route.
	from .all_logs import all_logs_blueprint
	app.register_blueprint(all_logs_blueprint, url_prefix="/all_logs")
	
	# Pull in all_hosts route.
	from .all_hosts import all_hosts_blueprint
	app.register_blueprint(all_hosts_blueprint, url_prefix="/all_hosts")
	
	# Pull in update_host route.
	from .update_host import update_host_blueprint
	app.register_blueprint(update_host_blueprint, url_prefix="/update_host")
	
	# Pull in delete_host route.
	from .delete_host import delete_host_blueprint
	app.register_blueprint(delete_host_blueprint, url_prefix="/delete_host")
	
	# Pull in clear_outage route.
	from .clear_outage import clear_outage_blueprint
	app.register_blueprint(clear_outage_blueprint, url_prefix="/clear_outage")
	
	return app
	
## DB Setup.
def create_database(app):
	if not path.exists("app/" + DB_NAME):
		db.create_all(app=app)
		print("[x] Created Database!")
