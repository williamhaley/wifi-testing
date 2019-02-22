#!/usr/bin/env bash

docker build . --tag williamhaley/wifi-testing

docker push williamhaley/wifi-testing
