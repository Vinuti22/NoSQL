// Проверка данных и RPO: сравнение подтверждённых ID (writer.log) с тем, что есть в базе.
const fs = require("fs");
const c = db.getSiblingDB("university_lab10").telemetry;
const lines = fs.readFileSync("results/writer.log", "utf8").split("\n").filter(l => l.startsWith("ACK "));
const acked = lines.map(l => +l.split(" ")[1]);
const inDb = new Set(c.find({ eventId: { $gte: 1000 } }, { eventId: 1, _id: 0 }).toArray().map(d => d.eventId));
const lost = acked.filter(id => !inDb.has(id));
print("всего документов:", c.countDocuments());
print("подтверждено (ACK):", acked.length, " найдено в БД:", inDb.size);
print("потеряно подтверждённых записей:", lost.length, lost.length ? JSON.stringify(lost) : "");
// максимальная пауза между соседними ACK = оценка времени недоступности записи при failover
let maxGap = 0, gapFrom = "", gapTo = "";
for (let i = 1; i < lines.length; i++) {
  const a = new Date(lines[i-1].split(" ")[2]), b = new Date(lines[i].split(" ")[2]);
  if (b - a > maxGap) { maxGap = b - a; gapFrom = a.toISOString(); gapTo = b.toISOString(); }
}
print("максимальная пауза между ACK, мс:", maxGap, "(", gapFrom, "->", gapTo, ")");
