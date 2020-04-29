#!/usr/bin/env python3

"""
execute_notify.py 

Execute a command and get a slack notification when it's done
"""

import subprocess
import datetime

config = {
	"slack_webhook_link": "link here"
}

def generate_slack_message_command(input_command, cmd_name="None"):
	message = f"Command `{input_command}` with name `{cmd_name}` finished at {str(datetime.datetime.now())}"
	slack_webhook_link = config["slack_webhook_link"]
	send_slack_command = """python3 -c 'import datetime;import json;import requests; requests.post("%s", headers={"Content-type": "application/json"}, data=json.dumps({"text": "%s"}))'""" % (slack_webhook_link, message)
	return send_slack_command

def run_command_preserve_output(command, cmd_name="None"):
	r_val = subprocess.Popen(command, shell=True)
	output, errors = r_val.communicate()
	slack_send = generate_slack_message_command(command, cmd_name)
	r_val = subprocess.Popen(slack_send, shell=True)
	output, errors = r_val.communicate()


def generate_bashscript():
	pass

def submit_to_cluster():
	pass


run_command_preserve_output("sleep 5")