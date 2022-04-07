import sqlite3

conn = sqlite3.connect("myDataBase.db")

print("CONNECTED TO DB")

def valid(email,password):
    qry = "select * from USERS where emial = '"+email+"' and password='"+password+"';"
    cur = conn.cursor()
    cur.execute(qry)
    rows = cur.fetchall()
    #print(rows)
    if(len(rows)==0):
        return False
    return True

print(valid("theblackboard.light@gmail.com","Sh@sh4nk"))