import sqlite3

class Patient:
    def init(self, name, age, contact):
        self.name = name
        self.age = age
        self.contact = contact

class Doctor:
    def init(self, name, specialty, contact):
        self.name = name
        self.specialty = specialty
        self.contact = contact

class Appointment:
    def init(self, patient, doctor, date, time):
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time

# Create a connection to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create tables for patients, doctors, and appointments
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        contact TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY,
        name TEXT,
        specialty TEXT,
        contact TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        doctor_id INTEGER,
        date TEXT,
        time TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (doctor_id) REFERENCES doctors (id)
    )
''')

conn.commit()
conn.close()