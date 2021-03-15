import sqlite3 as sql

con = sql.connect('book_tracking.db')

cursor = con.cursor()

cursor.execute("CREATE TABLE books(Title TEXT, Author TEXT, page_count INT, Genre TEXT, entry_date TEXT)")

con.close()