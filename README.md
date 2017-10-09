# WiFi Testing

Scripts and configurations to spin up machines for testing WiFi.

# Prerequisites

* lsusb
* tee
* python3
* Virtualbox with the latest extension pack
* Vagrant

# Build

Build the test VM.

```
TARGET=ubuntu-16.04 ./build.sh
```

# Test

Unplug your USB NIC.

Reset the VM before a test run.

```
./reset.py
```

Connect your USB NIC.

Go into the VM settings in VirtualBox and add the USB WiFi device.

Run tests against the VM.

```
./test.py
```

Analyze the results.

```
./analyze.py
```

# Citations

* [Connect a Usb device through Vagrant](https://code-chronicle.blogspot.com/2014/08/connect-usb-device-through-vagrant.html)
* https://www.vagrantup.com/docs/cli/snapshot.html
* https://linux.die.net/man/1/nmcli
* https://unix.stackexchange.com/questions/286721/get-wi-fi-interface-device-names
* https://superuser.com/questions/203272/list-only-the-device-names-of-all-available-network-interfaces
* https://unix.stackexchange.com/questions/87468/is-there-an-easy-way-to-programmatically-extract-ip-address
* https://www.mankier.com/1/iperf3
* https://bbs.nextthing.co/t/resolution-to-secrets-were-required-but-not-provided-and-a-follow-up-question/5120
* https://askubuntu.com/questions/8322/use-network-manager-to-connect-to-a-wifi-access-point-on-the-command-line
* https://fedoraproject.org/wiki/Networking/CLI
* https://unix.stackexchange.com/questions/184877/how-to-list-all-loadable-kernel-modules
