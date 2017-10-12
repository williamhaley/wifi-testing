#!/usr/bin/env bash

iperf3 --version | tail -1

echo "server: ${iperf_server}"
echo "client: ${ip}"

echo "kernel release: $(uname --kernel-release)"
echo "kernel version: $(uname --kernel-version)"
driver=$(sudo ethtool -i ${nic} | grep "^driver" | awk '{print $2}')
echo "driver: ${driver}"
echo "driver version: $(sudo ethtool -i ${nic} | grep "^version" | awk '{print $2}')"
echo "module filename: $(sudo modinfo $driver | grep "^filename" | awk '{print $2}')"
