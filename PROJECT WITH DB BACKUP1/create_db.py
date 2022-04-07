import sqlite3

conn = sqlite3.connect("myDataBase.db")

print("CONNECTED TO DB")

student_table_qry = """
CREATE TABLE IF NOT EXISTS USERS(
    id text PRIMARY KEY,
    name text NOT NULL,
    emial text NOT NULL,
    password text NOT NULL,
    type text NOT NULL
)
"""

all_calssrooms_qry="""
CREATE TABLE IF NOT EXISTS ALL_CLASSROOMS(
    id text PRIMARY KEY,
    name text NOT NULL,
    creator text NOT NULL
)
"""



conn.execute(student_table_qry)
print("USERS TABLE CREATED")
conn.execute(all_calssrooms_qry)
print("ALL_CLASSROOM TABLE CREATED")



