#!/usr/bin/env python3

"""
execute_notify.py

Execute a command and get a slack notification when it's done
"""

import subprocess
import urllib.parse


config = {
    "slack_webhook_link": "https://hooks.slack.com/services/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"
}


def generate_slack_message_command(input_command, cmd_name="None"):

    input_command = urllib.parse.quote_plus(input_command.replace(" ", "_"))
    cmd_name = urllib.parse.quote_plus(cmd_name.replace(" ", "_"))

    slack_webhook_link = config["slack_webhook_link"]
    send_slack_command = """/usr/bin/env python3 -c 'import datetime;import json;import requests; input_command="%s"; cmd_name="%s"; requests.post("%s", headers={"Content-type": "application/json"}, data=json.dumps({"text": f"Command `{input_command}` with name `{cmd_name}` finished at {str(datetime.datetime.now())}"}))'""" % (
        input_command, cmd_name, slack_webhook_link)
    return send_slack_command


def run_command_preserve_output(command, cmd_name="None"):
    try:
        r_val = subprocess.Popen(command, shell=True)
        output, errors = r_val.communicate()
    except KeyboardInterrupt:
        pass

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


def submit_to_cluster(command, cmd_name, job_name,
                      qsub_options="-q all.q"):
    bash_script_file = job_name+".sh"
    generate_bashscript(command, cmd_name, bash_script_file)
    r_val = subprocess.Popen(
        f"qsub {qsub_options} {bash_script_file}",
        shell=True)
    output, errors = r_val.communicate()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="Command to run and be notified about")
    parser.add_argument("--name", "-n", type=str, help="Name to label command with")
    parser.add_argument("--script", "-s", type=str, help="Save executible script instead of running interactively. Requires filename for script.")
    parser.add_argument("--blt", "-b", type=str, help="Submit immediately to BLT cluster. Requires job name")
    parser.add_argument("--qopts", "-q", type=str, help="SGE Queue to submit to. Will be passed to qsub. Example: gpu.q")
    args = parser.parse_args()

    name = args.name if args.name else "None"

    if not args.script and not args.blt:
        run_command_preserve_output(args.command, name)

    if args.script and args.blt:
        print("Cannot both save bash script and submit to BLT")
        exit(1)

    if args.script:
        generate_bashscript(args.command, name, args.script)

    if args.blt:
        qopts = "-q "+args.qopts if args.qopts else "-q all.q"
        submit_to_cluster(args.command, name, args.blt, qopts)



