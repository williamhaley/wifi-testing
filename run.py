#!/usr/bin/env python3

import subprocess
import re
import shlex

# Prompt to choose a USB device.
devices = (subprocess.check_output(["lsusb"])).splitlines()
devices = list(map(lambda device: device.decode("utf8"), devices))

for index, device in enumerate(devices):
	print("{:2d} | {}".format(index + 1, device))
device_index = int(input('\nSelect a device: '))

# Parse selection.
device = devices[device_index - 1]
device_ids = re.findall(r"([a-zA-Z0-9]{4}):([a-zA-Z0-9]{4})", device)[0]
vendor_id = device_ids[0]
product_id = device_ids[1]

target="ubuntu-16.04"
cwd="./ubuntu-16.04"

# https://stackoverflow.com/a/36971820/1459103
def parse_shell_var(line):
    return shlex.split(line, posix=True)[0].split('=', 1)

# Load config.
with open('ubuntu-16.04/Vagrantfile.conf', 'r') as f:
	configs = dict(parse_shell_var(line) for line in f if '=' in line)

# Restore base snapshot
snapshots = (subprocess.check_output(['vagrant', 'snapshot', 'list'], cwd=cwd)).decode("utf8")
if not re.match(r"" + re.escape(configs['SNAPSHOT_NAME']) + "", snapshots):
	print("Snapshot not found")
	exit(1)
subprocess.call(['vagrant', 'halt', '--force'], cwd=cwd)
subprocess.call(['VBoxManage', 'snapshot', configs['MACHINE_NAME'], 'restore', configs['SNAPSHOT_NAME']], cwd=cwd)

# Enable USB
subprocess.call(['VBoxManage', 'modifyvm', configs['MACHINE_NAME'], '--usb', 'on'], cwd=cwd)
subprocess.call(['VBoxManage', 'modifyvm', configs['MACHINE_NAME'], '--usbxhci', 'on'], cwd=cwd)

# Add filter for our device
subprocess.call(['VBoxManage', 'usbfilter', 'add', '0', '--name', 'USB WiFI NIC', '--target', configs['MACHINE_NAME'], '--vendorid', vendor_id, '--productid', product_id], cwd=cwd)

# Run the tests
subprocess.call(['vagrant', 'up'], cwd=cwd)
subprocess.call(['vagrant', 'ssh', '--', '-t', '/vbin/wifi-connect'], cwd=cwd)
subprocess.call(['vagrant', 'ssh', '--', '-t', '/vbin/wifi-test'], cwd=cwd)