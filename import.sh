#!/usr/bin/env bash
set -eu -o pipefail
[[ "${TRACE:-}" ]] && set -x

SERVER_DEFAULT="http://localhost:5000"

SERVER=${SERVER:-${SERVER_DEFAULT}}
patients_json=${1:-}
payments_json=${2:-}

if [[ -z "${patients_json}" ]] || [[ -z "${payments_json}" ]]; then
  echo "usage: [SERVER=api_server] ${0} patients_json payments_json"
  echo ""
  echo "positional arguments:"
  echo "  patients_json          JSON file with all patients"
  echo "  payments_json          JSON file with all payments"
  echo ""
  echo "environment arguments:"
  echo "  SERVER                 URL to API (optional, default is ${SERVER_DEFAULT})"
  echo ""
  exit 1
fi

echo "Upload patients:"
patients_url="${SERVER}/patients"
curl -f -X POST -H "Content-Type: application/json" -d "@${patients_json}" "${patients_url}"
echo

echo "Upload payments:"
payments_url="${SERVER}/payments"
curl -f -X POST -H "Content-Type: application/json" -d "@${payments_json}" "${payments_url}"
echo
