from flask import request, render_template, Blueprint 
from .update_db import update_db
from .models import Log, Alert

all_logs_blueprint = Blueprint("all_logs_blueprint", __name__)

# Reload route is.
@all_logs_blueprint.route('/<host>', methods=['GET'])

def index(host):

	args = request.args

	# Runs db check and update code.
	update_db()

	# Checks if Log table is populated yet.
	if Alert.query.first() == None:
		all_alerts = ""
	else:
		all_alerts = Alert.query.all()

	# Fetch all logs in decending order.
	all_logs = Log.query.filter_by(host=host).order_by(Log.date_created.desc()).all()

	if args.get("auto_refresh") == "true":
		return render_template('all_host_logs.html', host=host.capitalize(), entries=all_logs, alerts=all_alerts, refresh="true")
	else:
		return render_template('all_host_logs.html', host=host.capitalize(), entries=all_logs, alerts=all_alerts)
