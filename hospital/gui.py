import tkinter as tk
from tkinter import ttk
from modols import Patient, Doctor, Appointment

class HospitalManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("800x600")

        # Create tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True)

        # Patients tab
        self.patients_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.patients_tab, text="Patients")

        # Doctors tab
        self.doctors_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.doctors_tab, text="Doctors")

        # Appointments tab
        self.appointments_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.appointments_tab, text="Appointments")

        # Search tab
        self.search_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.search_tab, text="Search")

        # Create widgets for each tab
        self.create_patients_tab()
        self.create_doctors_tab()
        self.create_appointments_tab()
        self.create_search_tab()

    def create_patients_tab(self):
        # Create patient list treeview
        self.patient_list = ttk.Treeview(self.patients_tab, columns=("name", "age", "contact"))
        self.patient_list.pack(fill="both", expand=True)

        # Create patient entry fields
        self.patient_name_label = tk.Label(self.patients_tab, text="Name:")
        self.patient_name_label.pack()
        self.patient_name_entry = tk.Entry(self.patients_tab)
        self.patient_name_entry.pack()

        self.patient_age_label = tk.Label(self.patients_tab, text="Age:")
        self.patient_age_label.pack()
        self.patient_age_entry = tk.Entry(self.patients_tab)
        self.patient_age_entry.pack()

        self.patient_contact_label = tk.Label(self.patients_tab, text="Contact:")
        self.patient_contact_label.pack()
        self.patient_contact_entry = tk.Entry(self.patients_tab)
        self.patient_contact_entry.pack()

        # Create add patient button
        self.add_patient_button = tk.Button(self.patients_tab, text="Add Patient", command=self.add_patient)
        self.add_patient_button.pack()

        # Create delete patient button
        self.delete_patient_button = tk.Button(self.patients_tab, text="Delete Patient", command=self.delete_patient)
        self.delete_patient_button.pack()

    def create_doctors_tab(self):
        # Create doctor list treeview
        self.doctor_list = ttk.Treeview(self.doctors_tab, columns=("name", "specialty", "contact"))
        self.doctor_list.pack(fill="both", expand=True)

        # Create doctor entry fields
        self.doctor_name_label = tk.Label(self.doctors_tab, text="Name:")
        self.doctor_name_label.pack()
        self.doctor_name_entry = tk.Entry(self.doctors_tab)
        self.doctor_name_entry.pack()

        self.doctor_specialty_label = tk.Label(self.doctors_tab, text="Specialty:")
        self.doctor_specialty_label.pack()
        self.doctor_specialty_entry = tk.Entry(self.doctors_tab)
        self.doctor_specialty_entry.pack()

        self.doctor_contact_label = tk.Label(self.doctors_tab, text="Contact:")
        self.doctor_contact_label.pack()
        self.doctor_contact_entry = tk.Entry(self.doctors_tab)
        self.doctor_contact_entry.pack()

        # Create add doctor button
        self.add_doctor_button = tk.Button(self.doctors_tab, text="Add Doctor", command=self.add_doctor)
        self.add_doctor_button.pack()

        # Create delete doctor button
        self.delete_doctor_button = tk.Button(self.doctors_tab, text="Delete Doctor", command=self.delete_doctor)
        self.delete_doctor_button.pack()

    def create_appointments_tab(self):
        # Create appointment list treeview
        self.appointment_list = ttk.Treeview(self.appointments_tab, columns=("patient", "doctor", "date", "time"))
        self.appointment_list.pack(fill="both", expand=True)
        # Create appointment entry fields
        self.appointment_patient_label = tk.Label(self.appointments_tab, text=" minoo")