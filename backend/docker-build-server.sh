#!/bin/bash

set -e

cd "$(dirname "$0")"

docker build -t pptai-server -f server.Dockerfile .