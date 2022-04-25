import os
import slack
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response, Blueprint

# Slack docs on basic formatting.
# https://api.slack.com/reference/surfaces/formatting#basics

# Slack docs on advanced formatting using blocks.
# https://api.slack.com/block-kit/building

slack_bot = Blueprint("slack_bot", __name__)

# Load environment vars
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Defines app object
app = Flask(__name__)

SLACK_API_KEY = os.environ['SLACK_API_KEY'] 

client = slack.WebClient(token=SLACK_API_KEY)

BOT_ID = client.api_call("auth.test")['user_id']

def post_alert(host, last_known_status):
	Host = host.capitalize()

	# Hardcoded necessary slack information.
	channel_id = "YOUR_SLACK_CHANNEL_ID"
	user_id = "YOUR_SLACK_USER_ID"
#	channel_name = "YOUR_SLACK_CHANNEL_NAME"
	channel_name = "directmessage"


	# SlackAPI Block Better Formatting!
	alert_message_blocks = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":warning:Server Down!:warning:\n"
			}
		},

		{
			"type": "divider"
		},

		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Be advised, _*{Host}*_ has not reported in for the past 7+ minutes!\n\n"
			}
		},

		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":red_circle: _*Last Known Status*_"
			}
		},

		{
			"type": "divider"
		},

		{
			"type": "section",
			"fields": [
				# Left
				{
					"type": "mrkdwn",
					"text": "*Server*:"
				},
				# Right
				{
					"type": "mrkdwn",
					"text": f"{Host}"
				},
			]
		},

		{
			"type": "section",
			"fields": [
				# Left
				{
					"type": "mrkdwn",
					"text": "*Date/Time*:"
				},
				# Right
				{
					"type": "mrkdwn",
					"text": str(last_known_status.date_created)
				},
			]
		},

		{
			"type": "section",
			"fields": [
				# Left
				{
					"type": "mrkdwn",
					"text": "*Uptime*:"
				},
				# Right
				{
					"type": "mrkdwn",
					"text": str(last_known_status.uptime)
				},
			]

		},

		{
			"type": "section",
			"fields": [
				# Left
				{
					"type": "mrkdwn",
					"text": "*%Mem Used*:"
				},
				# Right
				{
					"type": "mrkdwn",
					"text": str(last_known_status.mem_used) + "%"
				},
			]

		},

		{
			"type": "section",
			"fields": [
				# Left
				{
					"type": "mrkdwn",
					"text": "*Avg Temp*:"
				},
				# Right
				{
					"type": "mrkdwn",
					"text": str(last_known_status.avg_temp) + "℃"
				},
			]

		},

		{
			"type": "section",
			"fields": [
				# Left
				{
					"type": "mrkdwn",
					"text": "*Misc Service Status*:"
				},
				# Right
				{
					"type": "mrkdwn",
					"text": str(last_known_status.misc_status)
				},
			]

		}, 

		{
			"type": "divider"
		},

		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": ":point_down:"
			}
		},

		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Click Here For More Information!"
					},
					"style": "primary",
					"url": f"https://monitor.bluesquare23.sh/all_logs/{host}"
				}
			]
		}
	]

	# Tries posting to slack channel (in a try / except in case doggo bot
	# can't talk to slacks servers for some reason).
	try:
		if channel_name == "directmessage":
			client.chat_postMessage(channel=f'@{user_id}', text=f"{Host} Down!", blocks=alert_message_blocks)
		else:
			client.chat_postMessage(channel=channel_id, text=f"{Host} Down!", blocks=alert_message_blocks)

	except slack.errors.SlackApiError:
		return "Error Posting To Slack\n", 501

	return Response(), 200

