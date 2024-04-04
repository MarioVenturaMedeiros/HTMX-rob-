import os
from tinydb import TinyDB

# Get the directory path of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'logs.json')

# Create the database
db = TinyDB(db_path)

# Define table
# logs_table = db.table('logs')

# Sample data
logs = [
    {"X": 200, "Y": 0, "Z": 50, "R": 0, "date": "2024-03-25"},
    {"X": 200, "Y": 0, "Z": 30, "R": 0, "date": "2024-03-27"},
    {"X": 1.5, "Y": 3.9, "Z": 4.0, "R": 88.0, "date": "2024-03-29"},
    {"X": 1.0, "Y": 4.0, "Z": 4.5, "R": 92.0, "date": "2024-03-31"},
    {"X": 1.3, "Y": 3.8, "Z": 4.2, "R": 87.5, "date": "2024-04-02"}
]

# Insert data into the database
# logs_table.insert_multiple(logs)
for log in logs:
    db.insert(log)
