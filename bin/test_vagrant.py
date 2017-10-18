#!/usr/bin/env python3

import subprocess
import re
import shlex
import datetime
import os
import sys
import json

target='ubuntu-16.04'
target_directory='./ubuntu-16.04'

now = datetime.datetime.utcnow()
formatted = now.strftime('%Y-%m-%d-%H-%M-%S')

subprocess.call(['vagrant', 'up'], cwd=target_directory)
subprocess.call(['vagrant', 'ssh', '--', '/vbin/wifi-connect.sh'], cwd=target_directory)
subprocess.call(['vagrant', 'ssh', '--', '/vbin/test.py'], cwd=target_directory)
