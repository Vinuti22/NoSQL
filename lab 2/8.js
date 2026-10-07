// 1. Создание 5 документов в коллекции doctors
db.doctors.insertMany([
  { _id: 201, name: "Д-р Арман Нурланов", specialty: "Allergist", cabinet: 104, experience: 12 },
  { _id: 202, name: "Д-р Гульнара Ибраева", specialty: "Therapist", cabinet: 201, experience: 8 },
  { _id: 203, name: "Д-р Виктор Ким", specialty: "Gastroenterologist", cabinet: 310, experience: 15 },
  { _id: 204, name: "Д-р Алия Бекова", specialty: "Dermatologist", cabinet: 108, experience: 5 },
  { _id: 205, name: "Д-р Кайрат Султанов", specialty: "Cardiologist", cabinet: 402, experience: 20 }
])

// 2. Привязка пациентов к врачам (прикрепление)
db.patients.updateOne(
  { patientId: 101 },
  { $set: { doctorIds: [201, 202] } }
)

db.patients.updateOne(
  { patientId: 102 },
  { $set: { doctorIds: [202, 203] } }
)

db.patients.updateOne(
  { patientId: 105 },
  { $set: { doctorIds: [201, 204] } }
)