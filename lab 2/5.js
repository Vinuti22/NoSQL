// 1. Поиск студентов, владеющих навыком "MongoDB"
db.students.find({ skills: "MongoDB" })

// 2. Поиск студентов, владеющих ОДНОВРЕМЕННО навыками "Java" и "MongoDB"
db.students.find({ skills: { $all: ["Java", "MongoDB"] } })

// 3. Добавление навыка "Docker" в массив skills для студента 1001
db.students.updateOne(
  { studentId: 1001 },
  { $push: { skills: "Docker" } }
)