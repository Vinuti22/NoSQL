// Непрерывная запись с w:majority — для измерения failover и RPO.
// Каждое подтверждённое (ACK) событие пишется в results/writer.log с временем.
// mongosh "<URI>" --file scripts/04_writer.js
const fs = require("fs");
const log = "results/writer.log";
fs.writeFileSync(log, "");
const c = db.getSiblingDB("university_lab10").telemetry;
let n = 1000;                       // eventId >= 1000 — «нагрузочные» записи
const end = Date.now() + 90 * 1000; // работаем 90 секунд
while (Date.now() < end) {
  n++;
  const t = new Date().toISOString();
  try {
    c.insertOne({ eventId: n, vehicleId: "BUS-100", ts: new Date(), speedKmh: 40, fuelPct: 50, lat: 43.22, lon: 76.85 },
                { writeConcern: { w: "majority", wtimeout: 3000 } });
    fs.appendFileSync(log, `ACK ${n} ${t}\n`);
  } catch (e) {
    fs.appendFileSync(log, `ERR ${n} ${t} ${String(e.message).replace(/\n/g, " ")}\n`);
  }
  sleep(200);
}
print("writer finished, last attempted id:", n);
