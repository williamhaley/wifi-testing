#!/usr/bin/env python3

import sys
import socket
import fcntl
import struct

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

if __name__ == "__main__":
	print(get_wireless_ip(sys.argv[1]))
