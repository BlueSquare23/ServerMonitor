from flask import render_template, Blueprint, request 
from .models import Host, Log, Alert, Outage 
from . import db
from .update_db import update_db

# Blueprinting to allow for modular code.
index = Blueprint("index", __name__)

# Webroot is just '/'.
@index.route('', methods=['GET'])

# Index page contents.
def home():
	# Re-runs db logic.
	update_db()

	# Gets top 10 recent_entries from Log table.
	recent_entries = Log.query.order_by(Log.date_created.desc()).limit(10)

	# Checks if Alert table is populated yet.
	if Alert.query.first() == None:
		all_alerts = ""
	else:
		all_alerts = Alert.query.all()

	# Checks if Outage table is populated yet.
	if Outage.query.first() == None:
		all_outages = ""
	else:
		all_outages = Outage.query.all()

	args = request.args
	if args.get("auto_refresh") == "true":
		return render_template('index.html', entries=recent_entries, alerts=all_alerts, outages=all_outages, refresh="true")
	else:
		return render_template('index.html', entries=recent_entries, alerts=all_alerts, outages=all_outages)
