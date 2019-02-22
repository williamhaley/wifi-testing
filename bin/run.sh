#!/usr/bin/env bash

set -e

/app/bin/test.py --server ${1} --logs-dir /app/logs/ --name "${2}"
