import sqlite3
from app import app

connection = sqlite3.connect("ticket.db")
cursor = connection.cursor()
cursor.execute("create table ticket (id INTEGER PRIMARY KEY AUTOINCREMENT, prio INTEGER, data TEXT, time INTEGER, status INTEGER, TIMESTAMP  DATETIME DEFAULT CURRENT_TIMESTAMP )")

item = (2, "hallo", 3, 0)
cursor.execute("insert into ticket (prio, data, time, status) values (?, ?, ?, ?)", item)

for row in cursor.execute("select * from ticket"):
    print(row)

connection.execute("SELECT * FROM ticket ORDER BY TIMESTAMP ASC")
connection.commit()
connection.close()
