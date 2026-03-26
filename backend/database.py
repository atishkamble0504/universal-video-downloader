import sqlite3

conn = sqlite3.connect("downloads.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS downloads (
id INTEGER PRIMARY KEY,
title TEXT,
filename TEXT
)
""")

conn.commit()