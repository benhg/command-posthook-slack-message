#!/bin/bash
ls -thor
python3 -c 'import datetime;import json;import requests; input_command="ls_-thor"; cmd_name="My_HPC_Job"; requests.post("slack link", headers={"Content-type": "application/json"}, data=json.dumps({"text": f"Command `{input_command}` with name `{cmd_name}` finished at {str(datetime.datetime.now())}"}))'

