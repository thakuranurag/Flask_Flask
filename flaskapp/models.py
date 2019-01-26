import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt

def insertUser(request):
    con = sql.connect("database.db")
   
    sqlQuery = "select username from userdata where (username ='" + request.form['username'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    
    if not row:
        cur.execute("INSERT INTO userdata (username,mobile,email,password) VALUES (?,?,?,?)", (request.form['username'], 
                   sha256_crypt.encrypt(request.form['password']),request.form['age'],request.form['gender'],request.form['interest']))
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


def retrieveUsers(): 
	con = sql.connect("database.db")
        # Uncomment line below if you want output in dictionary format
	#con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM users;")
	rows = cur.fetchall()
	con.close()
	return rows
  
