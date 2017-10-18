# WiFi Testing

Scripts and configurations for testing WiFi devices.

Tests can be run directly on a host machine, or against a VirtualBox VM.

You can either run `test.py` on your host, or use `test_vagrant.py` to run the tests from within a VM. **Run scripts from the root of this repo.**

_This project is a sloppy collection of scripts. Files are here for documentation, but do not expect the best quality. I would **not** recommend adapting/forking this for your own needs, as I expect the scripts to change drastically_.

# Prerequisites

* python3
* nmcli
* Vagrant
* VirtualBox

# Build

Build the test VM.

```
./bin/build-ubuntu.sh
```

# Test

Unplug your USB NIC.

Reset the VM before a test run.

```
./bin/reset_vagrant.py
```

Connect your USB NIC.

Go into the VM settings in VirtualBox and add the USB WiFi device.

_You could potentially make other customizations to the VM at this time if you like. For instance, you could install custom drivers or install certain packages. Note, any changes will be lost whenever you restore the snapshot._

Run tests against the VM.

```
./bin/test_vagrant.py
```

Analyze the results.

```
./bin/analyze.py
```

You can reset and retest as often as needed. Deleting the VM will require a rebuild.

# Citations

* [Connect a Usb device through Vagrant](https://code-chronicle.blogspot.com/2014/08/connect-usb-device-through-vagrant.html)
* [Vagrant Snapshot](https://www.vagrantup.com/docs/cli/snapshot.html)
* [nmcli](https://linux.die.net/man/1/nmcli)
* [Get Wi-Fi interface device names](https://unix.stackexchange.com/questions/286721/get-wi-fi-interface-device-names)
* [List only the device names of all available network interfaces](https://superuser.com/questions/203272/list-only-the-device-names-of-all-available-network-interfaces)
* [Is there an easy way to programmatically extract IP address? [duplicate]](https://unix.stackexchange.com/questions/87468/is-there-an-easy-way-to-programmatically-extract-ip-address)
* [iperf3 man page](https://www.mankier.com/1/iperf3)
* [Resolution to “Secrets were required, but not provided” and a follow up question](https://bbs.nextthing.co/t/resolution-to-secrets-were-required-but-not-provided-and-a-follow-up-question/5120)
* [Use Network-Manager to connect to a WiFi Access Point on the command-line](https://askubuntu.com/questions/8322/use-network-manager-to-connect-to-a-wifi-access-point-on-the-command-line)
* [Networking/CLI](https://fedoraproject.org/wiki/Networking/CLI)
* [How to list all loadable kernel modules?](https://unix.stackexchange.com/questions/184877/how-to-list-all-loadable-kernel-modules)
