"""
This file takes the billboard-200.db data and converts the resulting tables into separate csv files.

After running this script, run the csv_to_gz.py for further compression.
"""
import requests
import sqlite3
import csv

url = 'https://www.dropbox.com/s/ahog97hcatpiddk/billboard-200.db?dl=1'
response = requests.get(url)

with open('billboard-200.db', 'wb') as f:
    f.write(response.content)

conn = sqlite3.connect('billboard-200.db')

cursor = conn.cursor()

# Connects to SQLite Master file to get 'name' column where row type is 'table'
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    
    with open(f'{table_name}.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([description[0] for description in cursor.description])
        csv_writer.writerows(rows)

cursor.close()
conn.close()