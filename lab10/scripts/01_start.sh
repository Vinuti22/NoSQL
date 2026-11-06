#!/usr/bin/env bash
# Шаг 1: запуск трёх локальных mongod в фоне (учебный стенд, без аутентификации).
set -euo pipefail
source "$(dirname "$0")/config.sh"
mkdir -p "$DATA_DIR"
for i in 0 1 2; do
  p=${PORTS[$i]}; d="$DATA_DIR/rs$((i+1))"; mkdir -p "$d"
  mongod --replSet "$RS_NAME" --port "$p" --dbpath "$d" --bind_ip 127.0.0.1 \
         --logpath "$d/mongod.log" --fork --pidfilepath "$d/mongod.pid"
done
echo "Запущено 3 узла: ${PORTS[*]}"
