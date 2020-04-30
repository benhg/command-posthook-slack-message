#!/bin/bash
ls
python3 -c 'import datetime;import json;import requests; input_command="ls"; cmd_name="None"; requests.post("https://hooks.slack.com/services/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", headers={"Content-type": "application/json"}, data=json.dumps({"text": f"Command `{input_command}` with name `{cmd_name}` finished at {str(datetime.datetime.now())}"}))'

