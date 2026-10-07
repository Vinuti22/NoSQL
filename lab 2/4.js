// 1. Поиск всех студентов из города Almaty
db.students.find({ "contact.city": "Almaty" })

// 2. Поиск студентов из Almaty с GPA больше или равным 3.5 (запрос с дополнительным условием)
db.students.find({
  "contact.city": "Almaty",
  gpa: { $gte: 3.5 }
})

// 3. Поиск студентов, имеющих оценку за курс NoSQL выше 90 балов
db.students.find({
  "grades.course": "NoSQL",
  "grades.grade": { $gt: 90 }
})