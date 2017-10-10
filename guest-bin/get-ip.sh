#!/usr/bin/env bash

set -eo pipefail

NIC=$(/vbin/get-nic.sh)
IP=$(ifconfig "${NIC}" | grep "inet " | awk -F'[: ]+' '{ print $4 }')

echo $IP
