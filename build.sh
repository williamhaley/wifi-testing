#!/usr/bin/env bash

set -eo pipefail

if [ -z "$TARGET" ];
then
	echo "Specify a Target (ubuntu-16.04)"
	exit 1
fi

(
	cd "${TARGET}"
	source Vagrantfile.conf

	vagrant destroy
	vagrant up --no-provision > /dev/null
	vagrant provision
	vagrant halt
	vagrant snapshot save "default" "${SNAPSHOT_NAME}"
)
