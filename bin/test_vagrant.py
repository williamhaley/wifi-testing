#!/usr/bin/env python3

import subprocess
import re
import shlex
import datetime
import os
import sys
import json
import time
from argparse import ArgumentParser

target='ubuntu-16.04'
target_directory='./ubuntu-16.04'

now = datetime.datetime.utcnow()
formatted = now.strftime('%Y-%m-%d-%H-%M-%S')

parser = ArgumentParser(description='Test a WiFi card in Vagrant against an iperf3 server', prog='test_vagrant.py')
parser.add_argument('-n', '--name', required=True, dest='name', type=str, help='Name for this test run. Used to generate log file directory.')
args = parser.parse_args()

subprocess.call(['vagrant', 'up'], cwd=target_directory)

# Sleep. Let things settle a bit after the box comes up.
time.sleep(5)

subprocess.call(['vagrant', 'ssh', '--', '/vbin/wifi-connect.sh'], cwd=target_directory)
subprocess.call(['vagrant', 'ssh', '--', '/vbin/test.py', '--logs-dir', '/vlogs/', '--name', args.name, '--server', '192.168.0.116'], cwd=target_directory)
