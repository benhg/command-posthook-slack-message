#!/usr/bin/env python3

"""
execute_notify.py

Execute a command and get a slack notification when it's done
"""

import subprocess
import urllib.parse
import os
import json

config = {
    "slack_webhook_link": "GLOBAL LINK HERE"
}


def generate_slack_message_command(input_command, cmd_name="None", globalness=False):

    input_command = urllib.parse.quote_plus(input_command.replace(" ", "_"))
    cmd_name = urllib.parse.quote_plus(cmd_name.replace(" ", "_"))
    slack_webhook_link = 0
    try:
        if globalness:
            raise FileNotFoundError
        with open(os.path.expanduser("~/.slack_cmd_notifier.json")) as fh:
            slack_webhook_link = json.load(fh)["slack_webhook_link"]
    except FileNotFoundError as e:
        slack_webhook_link = config["slack_webhook_link"]

    send_slack_command = """/usr/bin/env python3 -c 'import datetime;import json;import requests; input_command="%s"; cmd_name="%s"; requests.post("%s", headers={"Content-type": "application/json"}, data=json.dumps({"text": f"Command `{input_command}` with name `{cmd_name}` finished at {str(datetime.datetime.now())}"}))'""" % (
        input_command, cmd_name, slack_webhook_link)
    return send_slack_command


def run_command_preserve_output(command, cmd_name="None", globalness=False):
    try:
        r_val = subprocess.Popen(command, shell=True)
        output, errors = r_val.communicate()
    except KeyboardInterrupt:
        pass

    slack_send = generate_slack_message_command(command, cmd_name, globalness=globalness)
    r_val = subprocess.Popen(slack_send, shell=True)
    output, errors = r_val.communicate()


def generate_bashscript(command, cmd_name, bash_script_file, globalness=False):
    """
    Generate a bash script of your command, followed by a notification.
    """
    with open(bash_script_file, "w") as fh:
        fh.write(f"#!/bin/bash\n")
        fh.write(f"{command}\n")
        fh.write(generate_slack_message_command(command, cmd_name, globalness=globalness))
        fh.write("\n\n")
    r_val = subprocess.Popen(f"chmod +x {bash_script_file}", shell=True)
    output, errors = r_val.communicate()


def submit_to_cluster(command, cmd_name, job_name,
                      qsub_options="-q all.q", globalness=False):
    bash_script_file = job_name+".sh"
    generate_bashscript(command, cmd_name, bash_script_file, globalness=globalness)
    r_val = subprocess.Popen(
        f"qsub {qsub_options} {bash_script_file}",
        shell=True)
    output, errors = r_val.communicate()

def configure():
    slack_link = input("Please enter your slack webhook link\n")
    config_template = {
    "slack_webhook_link": slack_link}
    with open(os.path.expanduser("~/.slack_cmd_notifier.json"), "w") as fh:
        fh.write(json.dumps(config_template))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="Command to run and be notified about")
    parser.add_argument("--name", "-n", type=str, help="Name to label command with", default="None")
    parser.add_argument("--script", "-s", type=str, help="Save executible script instead of running interactively. Requires filename for script.")
    parser.add_argument("--blt", "-b", type=str, help="Submit immediately to BLT cluster. Requires job name")
    parser.add_argument("--qopts", "-q", type=str, help="SGE Queue to submit to. Will be passed to qsub. Example: gpu.q")
    parser.add_argument("--config", "-c", action="store_true", help="Configure this app. Will start an interactive configuration process")
    parser.add_argument("--globality", "-g", action="store_true", help="Ignore any local configs and send to global channel")
    args = parser.parse_args()

    if args.config:
        configure()
        print("Thanks for configuring. On your next run of this progam, it will attempt to use your local configuration file")
        exit(1)

    if not args.script and not args.blt:
        run_command_preserve_output(args.command, name, globalness=args.globality)

    if args.script and args.blt:
        print("Cannot both save bash script and submit to BLT")
        exit(1)

    if args.script:
        generate_bashscript(args.command, name, args.script, globalness=args.globality)

    if args.blt:
        qopts = "-q "+args.qopts if args.qopts else "-q all.q"
        submit_to_cluster(args.command, name, args.blt, qopts, globalness=args.globality)



