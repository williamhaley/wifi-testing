#!/usr/bin/env bash

set -e

nic=$(lshw -c network -businfo | grep -i usb | awk '{print $2}')

wpa_supplicant \
	-B \
	-i ${nic} \
	-c /etc/wpa_supplicant/wpa_supplicant.conf \
	-Dwext

wpa_cli status

dhcpcd ${nic}

echo "Using kernel: $(uname -a)"
echo "WiFi device name is: ${nic}"
