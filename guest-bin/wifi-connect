#!/usr/bin/env bash

set -eo pipefail

source /vconf/Test.conf

NIC=$(/vbin/get-nic.sh)

echo "Using kernel: $(uname -a) on $(lsb_release -a)"
echo "WiFi NIC is: ${NIC}"
sudo nmcli device wifi connect "${SSID}" password "${PASSWORD}"
echo "Connected to WiFi: ${SSID}"
