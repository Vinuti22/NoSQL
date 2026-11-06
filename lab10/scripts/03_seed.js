// Шаг 3: 30 синтетических записей телеметрии (вариант 15), writeConcern majority.
// mongosh "mongodb://127.0.0.1:27101,127.0.0.1:27102,127.0.0.1:27103/?replicaSet=rsLab10" --file scripts/03_seed.js
const dbl = db.getSiblingDB("university_lab10");
dbl.telemetry.drop();
const docs = [];
const base = new Date("2026-11-01T08:00:00Z").getTime();
for (let i = 1; i <= 30; i++) {
  docs.push({
    eventId: i,                                   // уникальный идентификатор
    vehicleId: "BUS-" + (100 + (i % 5)),          // 5 синтетических ТС
    ts: new Date(base + i * 10000),
    speedKmh: 20 + (i * 7) % 60,
    fuelPct: 100 - i,
    lat: +(43.2220 + i * 0.001).toFixed(4),
    lon: +(76.8512 + i * 0.001).toFixed(4)
  });
}
dbl.telemetry.createIndex({ eventId: 1 }, { unique: true });
const r = dbl.telemetry.insertMany(docs, { writeConcern: { w: "majority", wtimeout: 5000 } });
print("inserted:", Object.keys(r.insertedIds).length);
print("count:", dbl.telemetry.countDocuments());
print("max eventId:", dbl.telemetry.find().sort({ eventId: -1 }).limit(1).next().eventId);
