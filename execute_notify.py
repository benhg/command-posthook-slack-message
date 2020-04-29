#!/usr/bin/env python3

"""
execute_notify.py 

Execute a command and get a slack notification when it's done
"""

config = {
	"slack_webhook_link": "link"
}

import datetime
import json

def generate_slack_message_command(input_command, cmd_name="None"):
	message = f"Command `{input_command}` with name `{cmd_name}` finished at {str(datetime.datetime.now())}"
	slack_webhook_link = config["slack_webhook_link"]
	send_slack_command = """python3 -c 'import datetime;import json;import requests; requests.post("%s", headers={"Content-type": "application/json"}, data=json.dumps({"text": "%s"}))'""" % (slack_webhook_link, message)
	return send_slack_command



print(generate_slack_message_command("ls"))