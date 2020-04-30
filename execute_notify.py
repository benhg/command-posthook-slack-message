#!/usr/bin/env python3

"""
execute_notify.py 

Execute a command and get a slack notification when it's done
"""

import subprocess
import datetime
import urllib.parse


config = {
	"slack_webhook_link": "slack link"
}

def generate_slack_message_command(input_command, cmd_name="None"):

	input_command = urllib.parse.quote_plus(input_command.replace(" ", "_"))
	cmd_name = urllib.parse.quote_plus(cmd_name.replace(" ", "_"))

	slack_webhook_link = config["slack_webhook_link"]
	send_slack_command = """python3 -c 'import datetime;import json;import requests; input_command="%s"; cmd_name="%s"; requests.post("%s", headers={"Content-type": "application/json"}, data=json.dumps({"text": f"Command `{input_command}` with name `{cmd_name}` finished at {str(datetime.datetime.now())}"}))'""" % (input_command, cmd_name, slack_webhook_link)
	return send_slack_command

def run_command_preserve_output(command, cmd_name="None"):
	r_val = subprocess.Popen(command, shell=True)
	output, errors = r_val.communicate()
	slack_send = generate_slack_message_command(command, cmd_name)
	r_val = subprocess.Popen(slack_send, shell=True)
	output, errors = r_val.communicate()


def generate_bashscript(command, cmd_name, bash_script_file):
	"""
	Generate a bash script of your command, followed by a notification.
	"""
	with open(bash_script_file, "w") as fh:
		fh.write(f"#!/bin/bash\n")
		fh.write(f"{command}\n")
		fh.write(generate_slack_message_command(command, cmd_name))
		fh.write("\n\n")
	r_val = subprocess.Popen(f"chmod +x {bash_script_file}", shell=True)
	output, errors = r_val.communicate()

def submit_to_cluster(command, cmd_name, bash_script_file, qsub_options="-q all.q"):
	generate_bashscript(command, cmd_name, bash_script_file)
	r_val = subprocess.Popen(f"qsub {qsub_options} {bash_script_file}", shell=True)
	output, errors = r_val.communicate()


submit_to_cluster("ls -thor", "My HPC Job",  "here.sh")