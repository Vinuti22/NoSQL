// Шаг 2: инициализация Replica Set.  mongosh --port 27101 --file scripts/02_init.js
rs.initiate({
  _id: "rsLab10",
  members: [
    { _id: 0, host: "127.0.0.1:27101" },
    { _id: 1, host: "127.0.0.1:27102" },
    { _id: 2, host: "127.0.0.1:27103" }
  ]
});
// ждём выбора PRIMARY
for (let i = 0; i < 30; i++) {
  if (rs.hello().isWritablePrimary) break;
  sleep(1000);
}
rs.status().members.forEach(m => print(m.name, m.stateStr));
