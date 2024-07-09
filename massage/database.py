import sqlite3

# Create a SQLite database connection
conn = sqlite3.connect("messages.db")
cursor = conn.cursor()

# Create a table