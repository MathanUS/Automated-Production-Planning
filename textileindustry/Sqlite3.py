import sqlite3


# Create a connection and cursor
conn = sqlite3.connect('Industry.db')
cursor = conn.cursor()
#cursor.execute('''DROP TABLE CUSTOMER''')
# Create a table for customers if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS CUSTOMER (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mail TEXT UNIQUE,
        phone TEXT,
        password TEXT
    )
''')
print('table customer created successfully')
cursor.execute('''SELECT * FROM CUSTOMER;''')
rows=cursor.fetchall()
print(rows)
# Commit changes and close the connection
conn.commit()
conn.close()

connection = sqlite3.connect('Industry.db')
cursor = connection.cursor()

#cursor.execute('''DROP TABLE TASK''')
cursor.execute('''CREATE TABLE IF NOT EXISTS TASK (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    taskId INTEGER,
                    machineId INTEGER,
                    duration INTEGER,
                    FOREIGN KEY(user_id) REFERENCES CUSTOMER(id));''')

print("SCHEDULING TASK TABLE CREATED SUCCESSFULLY")



sql_cmd16='''SELECT * FROM TASK;'''




cursor.execute(sql_cmd16)
rows=cursor.fetchall()
print(rows)

connection.commit()
connection.close()