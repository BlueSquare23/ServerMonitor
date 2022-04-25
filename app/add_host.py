from flask import Blueprint, render_template, redirect, request, flash
from . import db
from .models import Host
from werkzeug.security import generate_password_hash 

add_host_blueprint = Blueprint("add_host_blueprint", __name__)

@add_host_blueprint.route("/", methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		# Collect form data
		hostname = request.form.get("hostname")
		hostkey1 = request.form.get("hostkey1")
		hostkey2 = request.form.get("hostkey2")
		slack_notify = request.form.get("slack_notify")

		if slack_notify == None:
			slack_notify = "off"

		# Check if submitted form data for issues.
		hostname_exists = Host.query.filter_by(hostname=hostname).first()

		if hostname_exists:
			flash('Host already exits in db!', category='error')
		elif hostkey1 != hostkey2:
			flash('Hostkeys don\'t match!', category='error')
		elif len(hostkey1) < 8:
			flash('Hostkey is too short!', category='error')
		else:
			# Add the new_user to the database, then redirect home
			new_host = Host(hostname=hostname, hostkey=generate_password_hash(hostkey1, method='sha256'), slack_notify=slack_notify)
			db.session.add(new_host)
			db.session.commit()
			flash('Host Added!')
			return redirect('/')

	return render_template("add_host.html")
