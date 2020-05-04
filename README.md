# command-posthook-slack-message
Run an HPC job with a post-hook that makes a slack message on job exit

## Setup

To set up - 

1. Genrate a slack Incoming WebHook link
2. Clone this repo and put `execute_notify.py` somewhere executable/on path.
3. Edit `execute_notify.py` to add global slack link.
4. Optionally, create separate webhook links for separate user
5. Run `execute_notify.py` with `--config` option to save your personal link.

## Usage

To use:

```
usage: execute_notify [-h] [--name NAME] [--script SCRIPT] [--blt BLT]
                      [--qopts QOPTS] [--config] [--globality]
                      command

positional arguments:
  command               Command to run and be notified about

optional arguments:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  Name to label command with
  --script SCRIPT, -s SCRIPT
                        Save executible script instead of running
                        interactively. Requires filename for script.
  --blt BLT, -b BLT     Submit immediately to BLT cluster. Requires job name
  --qopts QOPTS, -q QOPTS
                        SGE Queue to submit to. Will be passed to qsub.
                        Example: gpu.q
  --config, -c          Configure this app. Will start an interactive
                        configuration process
  --globality, -g       Ignore any local configs and send to global channel
```
