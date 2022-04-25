from flask import Blueprint, request, make_response, jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash
from jsonschema import ValidationError
from flask_expects_json import expects_json
from .models import Host, Log, Alert, Outage 
from . import db
from .update_db import update_db

# Blueprinting to allow for modular code.
submit_blueprint = Blueprint("submit_blueprint", __name__)

# Return JSON for ValidationError errors.
@submit_blueprint.errorhandler(400)
def bad_request(error):
	if isinstance(error.description, ValidationError):
		original_error = error.description
		return make_response(jsonify({'error': original_error.message}), 400)
	# Else return HTML error as JSON.
	else:
		response = {
			"error code": error.code,
			"name": error.name,
			"description": error.description,
		}
		return response, 400

# Required JSON Schema for host submission data.
schema = {
    'type': 'object',
    'properties': {
		'host': {'type': 'string'},
		'host_key': {'type': 'string'},
		'ssh_status': {'type': 'string'},
		'misc_status': {'type': 'string'},
		'avg_temp': {'type': 'string'},
		'uptime': {'type': 'string'},
		'mem_used': {'type': 'string'}
	},
	'required': ['host', 'host_key', 'ssh_status', 'misc_status', 'avg_temp', 'uptime', 'mem_used']
}


# Route is /submit as definded in __init__.py.
@submit_blueprint.route('', methods=['POST'])
@expects_json(schema)

# Index page contents.
def submit():
	# Re-runs db logic.
	update_db()

	if(request.data):

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

		if host == None:
			return {"Post":"Failed", "Error":"Host not found!"}, 400

		if check_password_hash(host.hostkey, hostkey):
			new_entry = Log(host=hostname, ssh_status=ssh_status, misc_status=misc_status, avg_temp=avg_temp, uptime=uptime, mem_used=mem_used)
			try:
				db.session.add(new_entry)
				db.session.commit()
				return {"Post":"Success"}
			except:
				return {"Post":"Failed", "Error":"Issue writing to database!"}, 400
		else:
			return {"Post":"Failed", "Error":"Invalid hostkey for host!"}, 400
	else:
		return {"Post":"Failed", "Error":"Fatal Error! Bad Request!"}, 400

