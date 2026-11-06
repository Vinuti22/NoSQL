#!/usr/bin/env bash
# Общие настройки стенда. Только loopback 127.0.0.1.
export RS_NAME="rsLab10"
export PORTS=(27101 27102 27103)
export BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export DATA_DIR="$BASE_DIR/data"
export URI="mongodb://127.0.0.1:27101,127.0.0.1:27102,127.0.0.1:27103/?replicaSet=${RS_NAME}"
