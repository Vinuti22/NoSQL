#!/usr/bin/env bash
# Резервная копия и восстановление в ОТДЕЛЬНУЮ базу (без --drop).
set -euo pipefail
source "$(dirname "$0")/config.sh"
cd "$BASE_DIR"
rm -rf backup_lab10
mongodump --uri="$URI" --db=university_lab10 --out=./backup_lab10
mongorestore --uri="$URI" --nsFrom="university_lab10.*" --nsTo="university_restore10.*" ./backup_lab10/university_lab10
mongosh "$URI" --quiet --eval '
  const a=db.getSiblingDB("university_lab10").telemetry, b=db.getSiblingDB("university_restore10").telemetry;
  print("исходная:", a.countDocuments(), " восстановленная:", b.countDocuments());
  print("max eventId исходная:", a.find().sort({eventId:-1}).limit(1).next().eventId,
        " восстановленная:", b.find().sort({eventId:-1}).limit(1).next().eventId);'
