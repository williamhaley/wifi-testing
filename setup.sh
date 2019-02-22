#!/usr/bin/env bash

[[ $(id -u) = 0 ]] || { echo "run with sudo"; exit 1; }

set -e

apt update
apt install apt-transport-https ca-certificates curl software-properties-common --no-install-recommends --assume-yes
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
apt update
apt install docker-ce --no-install-recommends --assume-yes

sed -i 's|ExecStart=/usr/bin/dockerd.*|ExecStart=/usr/bin/dockerd --storage-driver=vfs -H fd://|' /lib/systemd/system/docker.service
systemctl daemon-reload
systemctl stop docker
systemctl start docker

user=${SUDO_USER:-$(whoami)}
usermod -aG docker ${user}

docker pull williamhaley/wifi-testing

# If we ever use Docker to connect to the WiFi network, you may need to disable
# NetworkManager on the host as that may conflict with manual wpa_supplicant /
# wpa_cli connections.
