from flask import redirect, Blueprint, flash
from .models import Host
from . import db

delete_host_blueprint = Blueprint("delete_host_blueprint", __name__)

# Outage blueprint decorator.
@delete_host_blueprint.route('/<int:id>', methods=['GET'])

def delete_host(id):
	host_to_delete = Host.query.get_or_404(id)
	flash('Cannot delete host on demo site!', category='error')
	return redirect('/all_hosts')
