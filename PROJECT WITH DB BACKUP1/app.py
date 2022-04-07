import re
from django.shortcuts import render
from flask import Flask, render_template, request,redirect ,session, url_for
#import send_otp
import capture_photos, create_folder, train_model

import sqlite3

# app _init_
app = Flask(__name__)
app.secret_key = "fiYy7oxau4PcfjVpjKNL"

conn = sqlite3.connect("myDataBase.db")
print("CONNECTED TO DB")
#WORKING FUNCTIONS 
def submit_to_database():

    with sqlite3.connect("myDataBase.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO USERS (id,name,emial,password,type)  VALUES (?,?,?,?,?)",(session["USERID"],session["NAME"],session["MAIL"],session["PASSWORD"],session["TYPE"]))
        con.commit()
        msg = "Record successfully added"

def send_mail(name,mail):
    import random
    num = str(random.randrange(100000, 999999))
    session["OTP"] = num
    #send_otp.send_mail(name,mail,num)
    return True

def create_user_table():
    newUser_qry="CREATE TABLE IF NOT EXISTS " + session["USERID"] + "(classrooms text NOT NULL);"
    with sqlite3.connect("myDataBase.db") as con:
        con.execute(newUser_qry)
    
def valid(email,password):
    qry = "select * from USERS where emial = '"+email+"' and password='"+password+"';"
    with sqlite3.connect("myDataBase.db") as con:
        cur = con.cursor()
        cur.execute(qry)
        rows = cur.fetchall()
        #print(rows)
        if(len(rows)==0):
            return False
        session["USERID"] = rows[0][0]
        session["NAME"] = rows[0][1]
        return True
    return False


#FUNCTIONS WITH ROOTS
@app.route("/")
@app.route("/home")
def home():
    session["SIGN_PAGE"] = -1
    session["FACE_PAGE"] = 0
    if(len(session["USERID"])!=0):
        return redirect(url_for("user",userID=session["USERID"]))
    return render_template("home.html")

@app.route("/SQL")
def SQL_TEST():
    #WORK HERE
    return render_template("SQL_TEXT.html")

@app.route("/<userID>")
def user(userID):
    return render_template("user.html",USERNAME=session["NAME"],ID=session["USERID"],TYPE=session["TYPE"])

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        mail = request.form["tv_mail"]
        password = request.form["tv_pass"]
        if valid(mail,password):
            print("WELCOME")
            return redirect(url_for("home"))
        return render_template("login.html")
    return render_template("login.html")

@app.route("/signup", methods=["POST","GET"])
def signup():
    print(session)
    if request.method == "POST":
        if session["SIGN_PAGE"] == -1:
            session["SIGN_PAGE"]=0
            return render_template("user_choice.html")


        if session["SIGN_PAGE"] == 0:
            session["SIGN_PAGE"]=1
            session["TYPE"] = request.form["btnradio"]
            return render_template("signup_1.html")


        if session["SIGN_PAGE"] == 1:
            session["NAME"] = request.form["tv_name"]
            session["MAIL"] = request.form["tv_mail"]
            send_mail(session["NAME"],session["MAIL"])
            session["SIGN_PAGE"]=2
            return render_template("signup_2.html")


        if session["SIGN_PAGE"] == 2:
            otp = str(request.form["tv_OTP"])
            if(otp == session["OTP"]):
                session["SIGN_PAGE"]=3
                return render_template("signup_3.html")
            session["SIGN_PAGE"]=2
            return render_template("signup_2.html")

        if session["SIGN_PAGE"] == 3:
            pass1 = request.form["tv_pass1"]
            pass2 = request.form["tv_pass2"]
            if pass1==pass2:     
                session["PASSWORD"] = pass1
                session["SIGN_PAGE"]=4
                return render_template("signup_4.html")
            session["SIGN_PAGE"]=3
            return render_template("signup_3.html")


        if session["SIGN_PAGE"] == 4:
            session["USERID"] = request.form["tv_user"]
            if(len(session["USERID"])!=0):
                if session["TYPE"] == "T":
                    submit_to_database()
                    create_user_table()
                    return redirect(url_for("home"))
                session["SIGN_PAGE"]=5
                return render_template("signup_5.html")
            session["SIGN_PAGE"]=4
            return render_template("signup_4.html")

    session["SIGN_PAGE"]=1
    return render_template("signup_1.html")


@app.route("/logout")
def logout():
    for x in session:
        session[x]=""    
    print(session)
    return redirect(url_for("home"))

@app.route("/face_signup", methods=["POST"])
def face_register():
    print(session)
    if session["FACE_PAGE"] == 0:
        session["cam_type"] = request.form["exampleRadios"]
        folder_loc = session["USERID"]+"/"
        create_folder.create_folder(folder_loc)
        session["FACE_PAGE"]=1
        return render_template("face_registeration_1.html")

        
    if session["FACE_PAGE"] == 1:
        capture_photos.capture_photos(5,session["cam_type"],session["USERID"])
        #openCamera.open_cam(session["cam_type"])
        session["FACE_PAGE"]=2
        return render_template("face_registeration_2.html")

    if session["FACE_PAGE"] == 2:
        capture_photos.capture_photos(5,session["cam_type"],session["USERID"])
        session["FACE_PAGE"]=3
        return render_template("face_registeration_3.html")

    if session["FACE_PAGE"] == 3:
        capture_photos.capture_photos(5,session["cam_type"],session["USERID"])
        train_model.train_model(session["USERID"])
        submit_to_database()
        create_user_table()
        return redirect(url_for("home"))
    return render_template("home.html")


#MAIN FUNCTION

if __name__ == "__main__":
    app.run(debug=True)



