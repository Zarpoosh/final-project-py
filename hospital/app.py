import tkinter as tk
from gui import HospitalManagementGUI

def main():
    root = tk.Tk()
    root.title("Hospital Management System")
    gui = HospitalManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()