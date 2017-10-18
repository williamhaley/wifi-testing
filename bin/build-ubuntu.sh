#!/usr/bin/env bash

(
	cd ubuntu-16.04
	source Vagrantfile.conf

	vagrant destroy
	vagrant up --no-provision > /dev/null
	vagrant provision
	vagrant halt
	vagrant snapshot save "default" "${SNAPSHOT_NAME}"
)
