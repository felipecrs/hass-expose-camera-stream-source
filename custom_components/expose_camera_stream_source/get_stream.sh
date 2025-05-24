#!/usr/bin/env bash

# This script is obsolete, but is kept for compatibility reasons.

set -eu

SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN:?"SUPERVISOR_TOKEN is not set, you need to run this script from an add-on."}"
entity_id="${1}"

exec curl -fsSL -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" "http://supervisor/core/api/camera_stream_source/${entity_id}"
