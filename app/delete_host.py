from flask import redirect, Blueprint, flash
from .models import Host
from . import db

delete_host_blueprint = Blueprint("delete_host_blueprint", __name__)

# Outage blueprint decorator.
@delete_host_blueprint.route('/<int:id>', methods=['GET'])

def delete_host(id):
	host_to_delete = Host.query.get_or_404(id)

	try:
		db.session.delete(host_to_delete)
		db.session.commit()
		flash('Host Deleted!', category='success')
		return redirect('/all_hosts')
	except:
		flash('Cannot Delete Host!', category='error')
		return redirect('/all_hosts')

