from flask import redirect, Blueprint, flash
from .models import Host
from . import db

update_host_blueprint = Blueprint("update_host_blueprint", __name__)

# Outage blueprint decorator.
@update_host_blueprint.route('/<int:id>', methods=['GET'])

def update_host(id):
	host_to_update = Host.query.get_or_404(id)

	try:
		if host_to_update.slack_notify == 'off':
			host_to_update.slack_notify = 'on'
		elif host_to_update.slack_notify == 'on':
			host_to_update.slack_notify = 'off'

		db.session.commit()
		flash('Host Updated!', category='success')
		return redirect('/all_hosts')
	except:
		flash('Cannot Update Host!', category='error')
		return redirect('/all_hosts')

