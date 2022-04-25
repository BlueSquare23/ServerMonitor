# Server Monitor

[Live Demo](https://monitor.bluesquare23.sh/)

## Overview / How it works

This project is a python Flask application built to keep tabs on a few home
servers. It works by accepting JSON POST requests from the host machines that
are being monitored. Each host machine reports back to the monitor by running a
bash script on a cronjob every two minutes. 

If a host has not 'phoned-home' for the past 7 minutes (aka 3 alert cycles) it
is considered "DOWN" and a red alert box is displayed on the monitoring
page(s). The alert box will remain visible on any of these monitoring pages
until that server is rebooted and starts reporting in again.

When an alert is created an "outage" report is also created. Unlike an alert,
an outage report has to be manually removed / cleared by a user of the web
page. This way the web app has a persistent record of any outages after a
server has been rebooted.

Likewise, when an outage report is generated a slack message is sent to the
person / slack channel specified.

## Installation & Setup

### Server Side

The server-side setup is pretty straight forward and this is run just like any
other flask app. Of course the instructions below are for spinning up the dev
version. Production setup involves extra steps.

* First clone the repo:

```
git clone https://github.com/BlueSquare23/ServerMonitor.git
```

* Then install the required python modules:

```
cd ServerMonitor
virtualenv venv	            # Virtual Env Optional
source venv/bin/activate    # Virtual Env Optional
pip3 install -r requirements.txt
```

* Then run the project:

```
python3 app.py
```

### Host Configuration

On each host that is being monitored you need to run some variation of the
following shell script to send the json status messages off to the monitor.

```
#!/usr/bin/env bash
# This script wraps a curl command which submits data to the ServerMonitor.

SSH_STATUS='SSH Status Cmd'
PLEX_STATUS='Plex Status Cmd'
AVERAGE_TEMP='Avg Temp Cmd'
UPTIME=`uptime`
MEM_USED='Mem Used Cmd'
HOSTKEY='Unique Host's Hostkey'

curl -s \
	-H "Content-Type: application/json" \
	-d "{ 
		\"host\":\"Your Host's Name\", 
		\"host_key\":\"$HOSTKEY\", 
		\"ssh_status\":\"$SSH_STATUS\", 
		\"misc_status\":\"Plex: $PLEX_STATUS\",
		\"avg_temp\":\"$AVERAGE_TEMP\", 
		\"uptime\":\"$UPTIME\", 
		\"mem_used\":\"$MEM_USED\" 
	}" \
	-X POST https://monitor.bluesquare23.sh/submit
```

## Technologies

* Language: [Python 3](https://www.python.org/)
* Web-Framework: [Flask](https://palletsprojects.com/p/flask/)
* Database: [SQLite](https://www.sqlite.org/index.html)
* ORM: [SQLAlchemy](https://www.sqlalchemy.org/)
* CSS: [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/)

