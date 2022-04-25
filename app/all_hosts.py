from flask import render_template, Blueprint
from .models import Host

all_hosts_blueprint = Blueprint("all_hosts_blueprint", __name__)

@all_hosts_blueprint.route('/', methods=['GET'])

def all_hosts():

	all_hosts = Host.query.all()

	return render_template('all_hosts.html', hosts=all_hosts)

