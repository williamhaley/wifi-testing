#!/usr/bin/env bash

nmcli device status | grep -i wifi | awk '{print $1}'
