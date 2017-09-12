#!/usr/bin/env bash

set -eo pipefail

{
sudo apt-get install --no-install-recommends --yes \
	network-manager \
	iperf3 \
	lshw \
	jq \
	wireless-tools

(
	cd /tmp
	wget https://raw.githubusercontent.com/philovivero/distribution/master/distribution.py
	sudo mv distribution.py /usr/local/bin/distribution
	sudo chmod +x /usr/local/bin/distribution
	sudo ln -s /usr/bin/python3 /usr/bin/python
)

# This kernel is what would be used by a new Ubuntu install. It includes the
# brcmfmac module
# https://wiki.archlinux.org/index.php/broadcom_wireless#History
sudo apt-get install --no-install-recommends --yes \
	linux-generic-hwe-16.04 \
	linux-headers-generic-hwe-16.04 \
	linux-image-generic-hwe-16.04

sudo systemctl enable network-manager.service 
sudo systemctl start network-manager.service
} &> /var/log/provision.log

echo "Done"

