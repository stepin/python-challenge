#!/usr/bin/env bash
set -eu -o pipefail
cd "$(dirname "$0")"
[[ "${TRACE:-}" ]] && set -x

./coverage.sh
coverage html
open htmlcov/index.html
