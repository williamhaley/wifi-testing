#!/usr/bin/env bash

set -eo pipefail

if [ -z "$TARGET" ];
then
	echo "Specify a Target (ubuntu-16.04)"
	exit 1
fi

STDOUT=/dev/null

usage() { echo "Usage: $0 [-v <vendorid>] [-p <productid>]" 1>&2; exit 1; }

while getopts ":v:p:" o; do
    case "${o}" in
        v)
            VENDOR_ID=${OPTARG}
            ;;
        p)
            PRODUCT_ID=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${VENDOR_ID}" ] || [ -z "${PRODUCT_ID}" ]; then
    usage
fi

if ! lsusb | grep -i "${VENDOR_ID}:${PRODUCT_ID}";
then
	echo "No USB device found with specified vendor and product ids."
	exit 1
fi

echo "Using vendorid ${VENDOR_ID} and productid ${PRODUCT_ID}"

# Run the rest in a subshell

(
cd "${TARGET}"
source Vagrantfile.conf

SNAPSHOT=$(vagrant snapshot list | grep -i "${SNAPSHOT_NAME}")

if [ -z "$SNAPSHOT" ];
then
	echo "Snapshot not found. Run build.sh first"
	exit 1
fi

vagrant halt --force > $STDOUT
# Using vagrant's snapshot mechanism, it also runs the VM.
# So do it through VBoxManage to avoid that so we can restore
# and then add the USB configuration options.
VBoxManage snapshot "${MACHINE_NAME}" restore "${SNAPSHOT_NAME}" > $STDOUT
VBoxManage modifyvm "${MACHINE_NAME}" --usb "on" > $STDOUT

if [ "${USB}" == "2" ];
then
	echo "Using USB 2.0"
	VBoxManage modifyvm "${MACHINE_NAME}" --usbehci "on" > $STDOUT
else
	echo "Using USB 3.0"
	VBoxManage modifyvm "${MACHINE_NAME}" --usbxhci "on" > $STDOUT
fi

VBoxManage usbfilter \
	add 0 \
	--name "USB WiFi NIC" \
	--target "${MACHINE_NAME}" \
	--vendorid "${VENDOR_ID}" \
	--productid "${PRODUCT_ID}" > $STDOUT

vagrant up > $STDOUT

# Connect to WiFi.
echo "Connect to WiFi"
vagrant ssh -- -t '/vbin/wifi-connect'

# Run WiFi performanc tests.
echo "Run performance tests"
vagrant ssh -- -t '/vbin/wifi-test'
)

