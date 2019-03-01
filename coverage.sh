#!/usr/bin/env bash
set -eu -o pipefail
cd "$(dirname "$0")"
[[ "${TRACE:-}" ]] && set -x

coverage run -m pytest
coverage report
