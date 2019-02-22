FROM ubuntu:18.04

RUN apt-get update && apt-get install --no-install-recommends --assume-yes \
	iperf3 \
	lshw \
	jq \
	build-essential \
	usbutils \
	python3 \
	&& apt clean && rm -rf /var/lib/apt/lists/*
