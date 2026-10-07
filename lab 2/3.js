// Добавление оценок студенту 1001
db.students.updateOne(
  { studentId: 1001 },
  { $set: { grades: [ { course: "NoSQL", grade: 90 }, { course: "Algorithms", grade: 85 } ] } }
)

// Добавление оценок студенту 1002
db.students.updateOne(
  { studentId: 1002 },
  { $set: { grades: [ { course: "NoSQL", grade: 95 }, { course: "Web Dev", grade: 92 } ] } }
)

// Добавление оценок студенту 1003
db.students.updateOne(
  { studentId: 1003 },
  { $set: { grades: [ { course: "NoSQL", grade: 98 }, { course: "Algorithms", grade: 94 }, { course: "Programming", grade: 90 } ] } }
)

// Добавление оценок студенту 1008
db.students.updateOne(
  { studentId: 1008 },
  { $set: { grades: [ { course: "Programming", grade: 100 }, { course: "NoSQL", grade: 96 } ] } }
)