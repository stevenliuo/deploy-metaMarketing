#!/bin/bash

set -e

cd "$(dirname "$0")"

docker build -t pptai-celery -f celery.Dockerfile .