#!/usr/bin/env bash

user=${SUDO_USER:-$(whoami)}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

nmcli device wifi connect "${3}" password "${4}"

# Run via sudo to get docker group without needing to log out/in on live system
sudo su - ${user} -c "
	docker run \
		-t -i \
		--rm \
		--net=host \
		--privileged \
		--cap-add=net_admin \
		--volume `pwd`:/app \
		williamhaley/wifi-testing \
		/app/bin/run.sh ${1} ${2}
"
