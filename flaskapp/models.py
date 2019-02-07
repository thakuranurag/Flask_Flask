import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt
from flask import jsonify
import os
import json

def insertUser(request):
    con = sql.connect("Flask_DB.db")
    print("yaha tak chal raha hai")
    print("user name " + request.form['username'])
    sqlQuery = "select mobile from userdata where (mobile ='" + request.form['mobile'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    
    if not row:
        cur.execute("INSERT INTO userdata (username,mobile,email,password,gender,location) VALUES (?,?,?,?,?,?)", (request.form['username'], 
                   request.form['mobile'],request.form['email'],sha256_crypt.encrypt(request.form['password'])
                   ,request.form['gender'],request.form['location']))
        con.commit()
        print "added user successfully"

       
    con.close()
    return not row


def authenticate(request):
    con = sql.connect("Flask_DB.db")
    sqlQuery = "select password from userdata where mobile = '%s'"%request.form['mobile']  
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    con.close()
    if row:
       return sha256_crypt.verify(request.form['password'], row[0])
    else:
       return False


def otp_verify(request):
    con = sql.connect("Flask_DB.db")
    cur = con.cursor()
    cur.execute("SELECT otp FROM otpdata where mobile='9826122862';")
    rows = cur.fetchall()
    if rows[0]==(request.form['otp']):
        con.close()
        return "success"
    else:
        con.close()
        return "failure"
	

def get_images():
    print("here madafaka")
    response_array=[]
    path=os.getcwd()
    print(path)
    con = sql.connect("Flask_DB.db")
        # Uncomment line below if you want output in dictionary format
    #con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT image FROM image_data where mobile='9826122862';")
    rows = cur.fetchall()
    for r in rows:
        response_array.append(str(r[0]))

    con.close()
    return response_array


def insertotp(request,otp,mobile):
    con = sql.connect("Flask_DB.db")
    print("yaha tak chal raha hai " + mobile + "  >>>  "+otp )
    sqlQuery = "select otp from otp_data where (mobile ='" + mobile + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    
    if not row:
        cur.execute("INSERT INTO otp_data (mobile,otp) VALUES (?,?)", (mobile,otp))
        con.commit()
        print "otp added successfully"
       
    con.close()
    return not row


def getOtp(request,mobile):
    con = sql.connect("Flask_DB.db")
    sqlQuery = "select otp from otp_data where (mobile ='" + mobile + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    
    if not row:
        cur.execute("INSERT INTO otp_data (mobile,otp) VALUES (?,?)", (mobile,otp))
        con.commit()
        print "otp added successfully"
       
    con.close()
    return not row





