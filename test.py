#!/usr/bin/env python3

import socket
import fcntl
import struct
import subprocess
import re
import datetime
import os
import sys
import json
import time
from optparse import OptionParser

def get_wireless_nic_name():
	"""
	Use nmcli to determine the wireless nic.

	Returns:
		Interface name string
	"""
	command = "nmcli device status | grep -i wifi | awk '{print $1}'"
	proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdoutdata, stderrdata = proc.communicate(input=None)
	if proc.returncode != 0:
		print("Error determining wireless NIC name.")
		return
	return stdoutdata.decode('utf8').strip()

def create_root_log_dir():
	"""
	Create the root log directory for this test run and return that path.

	The path is constructed relative to the current directory and uses the
	hostname and current time when determining the directory name.

	Returns:
		log_dir: Absolute path to the root log directory for this test run.
	"""
	now = datetime.datetime.utcnow()
	formatted = now.strftime('%Y-%m-%d-%H-%M-%S')
	current_dir = os.path.dirname(os.path.realpath(__file__))
	log_dir = current_dir + '/logs/' + socket.gethostname() + '-' + formatted
	os.makedirs(log_dir)
	return log_dir

def get_wireless_ip(nic_name):
	"""
	Get ip address of the specified network device.

	Args:
		nic_name: Name of the interface.

	Returns:

		IP address
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', bytes(nic_name[:15], 'utf-8'))
	)[20:24])

def module_info(module_name, field):
	"""
	Use modinfo to retrieve a specific field from the specified module.

	Args:
		module_name: Name of the module to query.
		field:       Field name to retrieve from module info.

	Returns:
		Description of the specified field for the module.
	"""
	return subprocess.check_output(['modinfo', '-F', field, module_name]).decode('utf8')

def log_system_info(log_dir, nic_name, server_address, client_address):
	"""
	Log a range of information about the nic and test machine.

	Args:
		log_dir:        Absolute path to the log directory for this test run.
		nic_name:       Name of the NIC being tested.
		server_address: Address of the iperf3 server used in testing.
		client_address: IP address of the test machine.
	"""
	info_log = open(log_dir + '/info.log', 'w')
	info_log.write("server: " + server_address + "\n")
	info_log.write("client: " + client_address + "\n")
	info_log.write("kernel release: " + subprocess.check_output(['uname', '--kernel-release']).decode('utf8'))
	info_log.write("kernel version: " + subprocess.check_output(['uname', '--kernel-version']).decode('utf8'))

	info_log.write("interface: " + subprocess.check_output(['cat', '/sys/class/net/' + nic_name + '/device/interface']).decode('utf8'))

	uevent = subprocess.check_output(['cat', '/sys/class/net/' + nic_name + '/device/uevent']).decode('utf8')
	match = re.search('^DRIVER=(.*)\n', uevent, re.MULTILINE)
	driver = match.group(1)
	match = re.search('^DEVTYPE=(.*)\n', uevent, re.MULTILINE)
	devtype = match.group(1)

	info_log.write("driver: " + driver + "\n")
	info_log.write("devtype: " + devtype + "\n")

	module_link_path = subprocess.check_output(['readlink', '-m', '/sys/class/net/' + nic_name + '/device/driver/module']).decode('utf8')
	module_name = module_link_path.strip().split('/')[-1].strip()

	info_log.write('module name: ' + module_name + '\n')
	info_log.write('module filename: ' + module_info(module_name, 'filename'))
	info_log.write('module version: ' + module_info(module_name, 'version'))
	info_log.write('module author: ' + module_info(module_name, 'author'))
	info_log.write('module description: ' + module_info(module_name, 'description'))

	info_log.close()

def run_tests(log_dir, client_ip, server_ip):
	download_log_dir = log_dir + '/downloads'
	upload_log_dir = log_dir + '/uploads'

	os.mkdir(download_log_dir)
	os.mkdir(upload_log_dir)

	download_summary_results = log_dir + '/download-results.txt'
	upload_summary_results = log_dir + '/upload-results.txt'

	# 2 hours
	test_time_in_seconds = 60 * 60 * 4

	test_start = datetime.datetime.utcnow()
	run = 1

	elapsed = (datetime.datetime.utcnow() - test_start).seconds

	while elapsed < test_time_in_seconds:
		print("Tests have been running for {:d} seconds. Will run until {:d} seconds elapsed.".format(elapsed, test_time_in_seconds))
		try:
			print('{:d} | download test'.format(run))
			download_test(download_log_dir, download_summary_results, client_ip, server_ip)
		except Exception as e:
			print('Error with download test.')
			print(e)
			time.sleep(2)

		time.sleep(2)

		try:
			print('{:d} | upload test'.format(run))
			upload_test(upload_log_dir, upload_summary_results, client_ip, server_ip)
		except Exception as e:
			print('Error with upload test.')
			print(e)

		time.sleep(2)

		run = run + 1
		elapsed = (datetime.datetime.utcnow() - test_start).seconds

def download_test(download_log_dir, summary_log_file_path, client_ip, server_ip):
	command = [
		'iperf3',
		'--bind',
		client_ip,
		'--reverse',
		'--json',
		'--format',
		'm',
		'--version4',
		'--client',
		server_ip
	]
	data = run_test(command, download_log_dir)

	# Write summary test information to stdout and summary log file.
	bits = data.get('end').get('sum_received').get('bits_per_second')
	mbps = bits / 1000000
	print('{:f} {:s}'.format(mbps, 'Mbps'))
	with open(summary_log_file_path, 'a') as summary_log_file:
		summary_log_file.write(str(mbps) + "\n")
		summary_log_file.close()

def upload_test(upload_log_dir, summary_log_file_path, client_ip, server_ip):
	command = [
		'iperf3',
		'--bind',
		client_ip,
		'--json',
		'--format',
		'm',
		'--version4',
		'--client',
		server_ip
	]
	data = run_test(command, upload_log_dir)
	# Write summary test information to stdout and summary log file.
	bits = data.get('end').get('sum_sent').get('bits_per_second')
	mbps = bits / 1000000
	print('{:f} {:s}'.format(mbps, 'Mbps'))
	with open(summary_log_file_path, 'a') as summary_log_file:
		summary_log_file.write(str(mbps) + "\n")
		summary_log_file.close()

def run_test(command, log_dir):
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdoutdata, stderrdata = proc.communicate(input=None)

	out = stdoutdata.decode('utf8')

	try:
		data = json.loads(out)
	except Exception as e:
		print('Error parsing json results. Error code is ' + proc.returncode)
		raise(stderrdata)

	error = data.get("error")
	if error != None:
		raise Exception(error)

	file_name = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S') + '.json'
	log_path = open(log_dir + '/' + file_name, 'w')
	log_path.write(out)
	log_path.close()

	return data

def main():
	parser = OptionParser()
	parser.add_option('-s', '--server', dest='server_address', type='string', help='Address of iperf3 server.')
	(options, args) = parser.parse_args()

	if options.server_address is None:
		parser.error('Server address not provided. View help for this script with --help')
		exit(1)
	else:
		server_address = options.server_address

	nic_name = get_wireless_nic_name()
	print("NIC name found:", nic_name)
	wifi_ip = get_wireless_ip(nic_name)
	print("WiFi ip found:", wifi_ip)

	log_dir = create_root_log_dir()

	log_system_info(log_dir, nic_name, server_address, wifi_ip)

	run_tests(log_dir, wifi_ip, server_address)

if __name__ == "__main__":
	main()
