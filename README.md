# Linux WiFi Performance and Reliability Testing

Scripts for testing USB WiFi devices on Linux

Note that the scripts in this repo are designed for **Ubuntu only**. Read the `Notes` section below for more details.

_This project is a sloppy collection of scripts. Files are here for documentation, but do not expect the best quality. I would **not** recommend adapting or forking this repository for your own needs, as I expect the scripts to change drastically over time. I am **not** an expert and I offer no guarantees or assurances and I do not take any liability whatsoever_.

# Setup

Clone this repo to your test machine.

```
git clone https://github.com/williamhaley/wifi-testing
```

Install required software and configure the host as necessary.

```
sudo ./setup.sh
```

Set up an iperf3 server on a separate machine on the same network. You may want to daemonize this or run it in something like tmux.

```
/usr/bin/iperf3 --server
```

Note the IP address of the test server as the client will need that for testing.

# Test

The test scripts will automatically choose whatever USB WiFi device they find. A TODO is to be able to pass the name of an explicit wireless interface.

You should disconnect/disable all other networking devices to avoid any confusion.

Run tests against your single USB WiFi device by passing the IP of your iperf server and arguments so that the host can connect to the network (which is simpler than having the container do so).

```
./test.sh <iperf.server.ip.address> <name for test run> <SSID> <Password>
```

Analyze the results.

```
./bin/analyze.py <path/to/results-file.txt> --scale-max 100
```

# Notes

Tests are intended to be run from within Docker for convenience and consistency. Docker uses the host kernel. Testing in Docker _should_ be almost identical to testing directly on the host OS (there may be some slight overhead, but I believe it should be minimal and inconsequential).

For the sake of consistency, I recommend always testing with the same host OS and host hardware. Ideally, boot to a live Ubuntu USB or CD-ROM on your test machine to guarantee the same results every time. If any of those parameters changes, I typically re-test *all* of my devices to guarantee reliable and consistent comparisons. You should not do _anything else_ on the host machine while running tests. No web browsing, tinkering, etc. Ideally, all testing should be done on an entirely independent WiFi network in order to totally isolate traffic.

At the lowest level, the tests are performed using iperf3. I cannot vouch for the reliability or superiority or inferiority of iperf3 as opposed to other network performance testing software, but I found that it was comparable to tests I performed with `netcat`.

I use Ubuntu for the host OS and the test OS due to its popularity. The goal is to test WiFi devices in a way that would apply to most Linux users. I use an ethernet-wired Raspberry Pi for the iperf3 server on my local network. The iperf3 server is wired directly to the router to eliminate any overhead and variables. The goal of this repo is to test the USB WiFI connection from the test machine to the router. Ideally, that is the only variable, and every other aspect of the test should be as consistent and reliable as possible.

# Citations

* [Run docker in ubuntu live disk](https://stackoverflow.com/questions/30248794/run-docker-in-ubuntu-live-disk)
* [Connect a Usb device through Vagrant](https://code-chronicle.blogspot.com/2014/08/connect-usb-device-through-vagrant.html)
* [Vagrant Snapshot](https://www.vagrantup.com/docs/cli/snapshot.html)
* [Get Wi-Fi interface device names](https://unix.stackexchange.com/questions/286721/get-wi-fi-interface-device-names)
* [List only the device names of all available network interfaces](https://superuser.com/questions/203272/list-only-the-device-names-of-all-available-network-interfaces)
* [Is there an easy way to programmatically extract IP address? [duplicate]](https://unix.stackexchange.com/questions/87468/is-there-an-easy-way-to-programmatically-extract-ip-address)
* [iperf3 man page](https://www.mankier.com/1/iperf3)
* [Resolution to “Secrets were required, but not provided” and a follow up question](https://bbs.nextthing.co/t/resolution-to-secrets-were-required-but-not-provided-and-a-follow-up-question/5120)
* [Use Network-Manager to connect to a WiFi Access Point on the command-line](https://askubuntu.com/questions/8322/use-network-manager-to-connect-to-a-wifi-access-point-on-the-command-line)
* [Networking/CLI](https://fedoraproject.org/wiki/Networking/CLI)
* [How to list all loadable kernel modules?](https://unix.stackexchange.com/questions/184877/how-to-list-all-loadable-kernel-modules)
