from flask import Blueprint, render_template, redirect, request, flash
from . import db
from .models import Host
from werkzeug.security import generate_password_hash 

add_host_blueprint = Blueprint("add_host_blueprint", __name__)

@add_host_blueprint.route("", methods=['GET', 'POST'])
def add_host():
	if request.method == 'POST':
		# Collect form data
		hostname = request.form.get("hostname")
		hostkey1 = request.form.get("hostkey1")
		hostkey2 = request.form.get("hostkey2")
		slack_notify = request.form.get("slack_notify")

		if slack_notify == None:
			slack_notify = "off"

		# Makesure form is filled out.
		if bool(hostname) != True or bool(hostkey1) != True or bool(hostkey2) != True:
			flash('Please enter all required information!', category='error')
			return render_template("add_host.html")

		# Check if submitted form data for issues.
		hostname_exists = Host.query.filter_by(hostname=hostname).first()

		if hostname_exists:
			flash('Host already exits in db!', category='error')
		elif hostkey1 != hostkey2:
			flash('Hostkeys don\'t match!', category='error')
		elif len(hostkey1) < 8:
			flash('Hostkey is too short!', category='error')
		else:
			flash('Cannot add host on demo site!', category='error')
			return redirect('/add_host')

	return render_template("add_host.html")
