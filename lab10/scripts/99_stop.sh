#!/usr/bin/env bash
# Остановка только своих процессов стенда (по pid-файлам).
source "$(dirname "$0")/config.sh"
for i in 1 2 3; do f="$DATA_DIR/rs$i/mongod.pid"; [ -f "$f" ] && kill "$(cat "$f")" 2>/dev/null || true; done
