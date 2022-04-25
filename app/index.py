from flask import render_template, Blueprint, request 
from werkzeug.security import check_password_hash
from .models import Host, Log, Alert, Outage 
from . import db
from .update_db import update_db

# Blueprinting to allow for modular code.
index = Blueprint("index", __name__)

# Webroot is just '/'.
@index.route('/', methods=['POST', 'GET'])

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

	if request.method == 'POST':

		poll = request.get_json()

		hostname = poll['host']
		hostkey = poll['host_key']
		ssh_status = poll['ssh_status']
		misc_status = poll['misc_status']
		avg_temp = poll['avg_temp']
		uptime = poll['uptime']
		mem_used = poll['mem_used']

		# Check hostkey for host before allowing post.
		host = Host.query.filter_by(hostname=hostname).first()

		if host:
			if check_password_hash(host.hostkey, hostkey):
				new_entry = Log(host=hostname, ssh_status=ssh_status, misc_status=misc_status, avg_temp=avg_temp, uptime=uptime, mem_used=mem_used)
				try:
					db.session.add(new_entry)
					db.session.commit()
					return '{"Post":"Success"}'
				except:
					return '{"Post":"Failed", "Error":"Issue writing to database!"}'
			else:
				return '{"Post":"Failed", "Error":"Invalid hostkey for host!"}'
		else:
			return '{"Post":"Failed", "Error":"Unknown Host"}'
	else:
		args = request.args
		if args.get("auto_refresh") == "true":
			return render_template('index.html', entries=recent_entries, alerts=all_alerts, outages=all_outages, refresh="true")
		else:
			return render_template('index.html', entries=recent_entries, alerts=all_alerts, outages=all_outages)
