// 1. Создание документов в коллекции courses
db.courses.insertMany([
  { _id: 501, name: "NoSQL", credits: 5, department: "IS" },
  { _id: 502, name: "Algorithms", credits: 5, department: "CS" },
  { _id: 503, name: "Programming", credits: 6, department: "CS" },
  { _id: 504, name: "Web Dev", credits: 4, department: "IS" },
  { _id: 505, name: "DevOps", credits: 5, department: "SE" }
])

// 2. Связывание студентов с курсами по ID (Referencing)
db.students.updateOne(
  { studentId: 1001 },
  { $set: { courseIds: [501, 502, 505] } }
)

db.students.updateOne(
  { studentId: 1003 },
  { $set: { courseIds: [501, 502, 503] } }
)