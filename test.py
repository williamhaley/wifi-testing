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

current_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = current_dir + '/logs/' + formatted

os.mkdir(log_dir)
os.mkdir(log_dir + '/downloads')
os.mkdir(log_dir + '/uploads')

def run_test(command, summary_log_file_path, key):
	args = shlex.split(command)
	proc = subprocess.Popen(args, cwd=target_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	with open(summary_log_file_path, 'a') as summary_log_file:
		stdoutdata, stderrdata = proc.communicate(input=None)

		if proc.returncode != 0:
			print("Unexpected error occurred (probably NIC not detected in VM. Kill this script, use a different USB port, and re-connect NIC)")
			return

		out = stdoutdata.decode('utf8')
		data = json.loads(out)

		error = data.get("error")
		if error != None:
			raise Exception(error)

		# Upload
		if key == 'sum_sent':
			test_log_dir = 'uploads'
		# Download
		elif key == 'sum_received':
			test_log_dir = 'downloads'

		file_name = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S') + '.json'

		# Write complete log file for this test iteration.
		test_log = open(log_dir + '/' + test_log_dir + '/' + file_name, 'w')
		test_log.write(out)
		test_log.close()

		# Write summary test information to stdout and summary log file.
		bits = data.get('end').get(key).get('bits_per_second')
		mbps = bits / 1000000
		print('{:f} {:s}'.format(mbps, 'Mbps'))
		summary_log_file.write(str(mbps) + "\n")
		summary_log_file.close()

vagrant_up_log = open(log_dir + '/vagrant.log', 'w')
subprocess.call(['vagrant', 'up'], cwd=target_directory, stdout=vagrant_up_log, stderr=vagrant_up_log)

wifi_connect_log = open(log_dir + '/wifi-connect.log', 'w')
subprocess.call(['vagrant', 'ssh', '--', '/vbin/wifi-connect'], cwd=target_directory, stdout=wifi_connect_log, stderr=wifi_connect_log)

info_log = open(log_dir + '/info.log', 'w')
subprocess.call(['vagrant', 'ssh', '--', '/vbin/info'], cwd=target_directory, stdout=info_log, stderr=info_log)

download_log_dir = log_dir + '/download-results.txt'
upload_log_dir = log_dir + '/upload-results.txt'

# 2 hours
test_time_in_seconds = 60 * 60 * 2

test_start = datetime.datetime.utcnow()
run = 1

def elapsed(start):
	return (datetime.datetime.utcnow() - test_start).seconds

while elapsed(test_start) < test_time_in_seconds:
	print("Tests have been running for {:d} seconds. Will run until {:d} seconds elapsed.".format(elapsed(test_start), test_time_in_seconds))
	try:
		print('{:d} | download test'.format(run))
		run_test('vagrant ssh -- /vbin/wifi-download-test.sh', download_log_dir, 'sum_received')
		print('{:d} | upload test'.format(run))
		run_test('vagrant ssh -- /vbin/wifi-upload-test.sh', upload_log_dir, 'sum_sent')
	except Exception as e:
		print(e)

	run = run + 1
