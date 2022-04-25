from .models import Host, Log, Alert, Outage
from datetime import datetime, timedelta 
from . import db
from .slackapi import post_alert

# The amount of time in minutes before a host is reported as down.
timeframe = 7

def update_db():
	# Returns the most recently logged entry for any host from the Log table.
	def get_newest_entry_for(host):
		return Log.query.filter_by(host=host).order_by(Log.date_created.desc()).first()

	# Returns True or False depending on if entry for host exists.
	def check_entry(host):
		return Log.query.filter_by(host=host).first() is not None

	def check_and_notify_slack(host):
		# If slack_notify is enabled for host, 
		if Host.query.filter_by(hostname=host).first().slack_notify == "on":
			# then send slack outage message.
			post_alert(host, get_newest_entry_for(host))

	# Check's and trims Log table if number of logs gets too large.
	def trim_db():
		if Log.query.count() > 10000:
			#print("Trimming DB...")
			oldest_id = Log.query.order_by(Log.date_created).first().id
			for i in range(5000):
				id_to_delete = oldest_id + i
				Log.query.filter_by(id=id_to_delete).delete()
				db.session.commit()

	# Initialize empty hosts list.
	hosts = []

	# Checks if Host table is populated and if so appends hostnames to hosts
	# list.
	if Host.query.first() != None:
		for host in Host.query.all():
			hosts.append(host.hostname)
	
	# Get timestamp from timeframe minutes ago.
	time_frame_ago = datetime.now() - timedelta(minutes=timeframe)

	for host in hosts:
		# Checks if Log table is populated yet and if empty if so return
		# nothing.
		if Log.query.first() == None:
			return ""
		else:

			# Trim log database.
			trim_db()

			# Check if there is an entry for host and if so get last entry
			# time.
			if check_entry(host):
				# Most recent entry time.
				last_entry_time = get_newest_entry_for(host).date_created

				# If the last reported time from the host is more than 10
				# mintes ago, create a new alert in the database. 

				# Don't let the direction of the carrot fool you. In this
				# context 'less than' means 'further back in time than'.
				if last_entry_time < time_frame_ago:

					# If there is already an alert for host overwrite it.
					# There should only ever be one alert per host. Helps while
					# developing to prevent alerts table from becoming bloated.
					if Alert.query.filter_by(host=host).first() is not None:	
						host_alert = Alert.query.filter_by(host=host).first()
						host_alert.last_logged=get_newest_entry_for(host).date_created	
						db.session.commit()

					# Else create new Alert entry.
					else:	
						new_alert_entry = Alert(host=host, last_logged=get_newest_entry_for(host).date_created)
						db.session.add(new_alert_entry)
						db.session.commit()

					# Add new outage entry at the same time as alert entry.
					# Except there can be more than one outage reported at any
					# given time. Also don't re-add the same most recent outage.

					# If the Outage table is empty,
					if Outage.query.first() == None:
						print(type(get_newest_entry_for(host)))

						# Check db notification perfs for host and if set
						# notify slack of newest outage.
						check_and_notify_slack(host)

						# Add new outage event to Outage table.
						new_outage_entry = Outage(host=host, last_logged=get_newest_entry_for(host).date_created)
						db.session.add(new_outage_entry)
						db.session.commit()
					else:

						# If outage timestamp is not already in Outage table
						# add outage event (but don't duplicate).

						if Outage.query.filter_by(host=host).filter_by(last_logged=last_entry_time).first() == None:
							# Check db notification perfs for host and if set
							# notify slack of newest outage.
							check_and_notify_slack(host)

							# Add new outage event to Outage table.
							new_outage_entry = Outage(host=host, last_logged=get_newest_entry_for(host).date_created)
							db.session.add(new_outage_entry)
							db.session.commit()

				# If host's last entry time is newer than 10 min ago then delete
				# the alert entry for said host.
				if last_entry_time > time_frame_ago:
					if Alert.query.filter_by(host=host).first() is not None:
						host_id = Alert.query.filter_by(host=host).one().id
						Alert.query.filter_by(id=host_id).delete()
						db.session.commit()
	
