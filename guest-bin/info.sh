#!/usr/bin/env bash

source /vconf/Test.conf

iperf3 --version | tail -1

echo "server: ${IPERF_SERVER}"
NIC=$(/vbin/get-nic.sh)
IP=$(/vbin/get-ip.sh)
echo "client: ${IP}"

echo "kernel release: $(uname --kernel-release)"
echo "kernel version: $(uname --kernel-version)"
DRIVER=$(sudo ethtool -i ${NIC} | grep "^driver" | awk '{print $2}')
echo "driver: ${DRIVER}"
echo "driver version: $(sudo ethtool -i $NIC | grep "^version" | awk '{print $2}')"
echo "module filename: $(sudo modinfo $DRIVER | grep "^filename" | awk '{print $2}')"
