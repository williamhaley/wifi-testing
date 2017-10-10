#!/usr/bin/env bash

set -eo pipefail

source /vconf/Test.conf

START=$(date)

IP=$(/vbin/get-ip.sh)

if [ -z "$IP" ];
then
	echo "Cannot determine client IP"
	exit 1
fi

if [ -z "$IPERF_SERVER" ];
then
	echo "No IPERF_SERVER specified"
	exit 1
fi

iperf3 \
	--bind "${IP}" \
	--reverse \
	--json \
	--format m \
	--version4 \
	--client "${IPERF_SERVER}"
