from flask_login import UserMixin
from datetime import datetime
from . import db

class Host(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	hostname = db.Column(db.String(150), unique=True)
	hostkey = db.Column(db.String(150))
	slack_notify = db.Column(db.String(150))
	date_created = db.Column(db.DateTime(timezone=True), default=datetime.now)

class Log(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	host = db.Column(db.String(150))
	ssh_status = db.Column(db.String(200))
	misc_status = db.Column(db.String(200))
	avg_temp = db.Column(db.String(200))
	uptime = db.Column(db.String(200))
	mem_used = db.Column(db.String(200))
	date_created = db.Column(db.DateTime(timezone=True), default=datetime.now)

class Alert(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	host = db.Column(db.String(150))
	last_logged = db.Column(db.String(200))

class Outage(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	host = db.Column(db.String(150))
	last_logged = db.Column(db.String(200))
