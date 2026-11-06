#!/usr/bin/env bash
# Полный прогон сценария А одной командой (Linux/macOS/Git Bash/WSL).
# Результаты сохраняются в results/. Скриншоты сделайте вручную.
set -euo pipefail
source "$(dirname "$0")/config.sh"
cd "$BASE_DIR"; mkdir -p results

bash scripts/01_start.sh
sleep 3
mongosh --port 27101 --quiet --file scripts/02_init.js | tee results/01_status_before.txt
mongosh "$URI" --quiet --file scripts/03_seed.js         | tee results/02_seed.txt

PRIMARY_PORT=$(mongosh "$URI" --quiet --eval 'print(rs.hello().primary.split(":")[1])')
PRIMARY_IDX=$((PRIMARY_PORT-27101+1))
echo "PRIMARY: порт $PRIMARY_PORT" | tee results/03_primary.txt

mongosh "$URI" --quiet --file scripts/04_writer.js > results/writer_stdout.txt 2>&1 &
WRITER=$!
sleep 15

# t0 — остановка ТОЛЬКО своего primary (по pid-файлу стенда)
PIDFILE="$DATA_DIR/rs${PRIMARY_IDX}/mongod.pid"
T0=$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)
kill "$(cat "$PIDFILE")"
echo "t0 (остановка primary): $T0" | tee results/04_t0_t1.txt

# t1 — появление нового PRIMARY
T1=""; NP=""
for i in $(seq 1 120); do
  NP=$(mongosh "$URI" --quiet --eval 'try{print(rs.hello().primary||"")}catch(e){print("")}' 2>/dev/null || true)
  if [ -n "$NP" ] && [ "$NP" != "127.0.0.1:${PRIMARY_PORT}" ]; then
    T1=$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ); break
  fi
  sleep 0.25
done
echo "t1 (новый PRIMARY $NP): $T1" | tee -a results/04_t0_t1.txt
mongosh "$URI" --quiet --eval 'rs.status().members.forEach(m=>print(m.name,m.stateStr))' | tee results/05_status_after_election.txt

sleep 10
# возврат остановленного узла с теми же dbpath/портом/replSet
mongod --replSet "$RS_NAME" --port "$PRIMARY_PORT" --dbpath "$DATA_DIR/rs${PRIMARY_IDX}" \
  --bind_ip 127.0.0.1 --logpath "$DATA_DIR/rs${PRIMARY_IDX}/mongod.log" --fork --pidfilepath "$PIDFILE" --logappend
sleep 15
mongosh "$URI" --quiet --eval 'rs.status().members.forEach(m=>print(m.name,m.stateStr))' | tee results/06_status_after_rejoin.txt

wait $WRITER || true
mongosh "$URI" --quiet --file scripts/05_check.js | tee results/07_rpo_check.txt
bash scripts/06_backup_restore.sh | tee results/08_backup_restore.txt
echo "Готово. Остановить стенд: bash scripts/99_stop.sh"
