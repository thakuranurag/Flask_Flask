from flask import Flask
from flask import render_template
import models as dbHandler
from flask import request
from flask import redirect, url_for
from flask import session
from flask import jsonify
from flask_mail import Mail, Message
import json,random
from datetime import datetime
import requests
import os
import unirest


app = Flask(__name__ )
app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')


app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'connectevery1@gmail.com',
    MAIL_PASSWORD = 'ursqanoktpbxwowq',
))

mail = Mail(app)

@app.route('/')
def some():
    return "gegsgs"

@app.route('/send-mail/')
def send_mail():
    msg = mail.send_message(
        'Send Mail tutorial!',
        sender='connectevery1@gmail.com',
        recipients=['anuragt0007@gmail.com'],
        body="Congratulations you've succeeded!"
    )
    return 'success'

########################### root ###########################

@app.route('/')
def index():
   if 'username' in session:
      return render_template("index.html", logged_in = True,  username=session['username'])
   else:
      return render_template("index.html", logged_in = False,  username=None)



###########################  login ################################################################


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'mobile' in session:
        return redirect(url_for('home'))

    elif request.method == 'POST':
        if dbHandler.authenticate(request):
            session['mobile'] = request.form['mobile']
            msg = "successful login"
            return redirect(url_for('home'))
        else:
            msg ="login failed"
            return render_template("result.html", message=msg)

    return render_template('login.html')



######################### register ################################################
@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'mobile' in session:
        return redirect(url_for('home'))

    if request.method=='POST':
        if dbHandler.insertUser(request):
            msg = "success in adding user"
        else:
            msg = "failed to add user"
        session['mobile'] = request.form['mobile']
        otp=random.randint(1000, 9999)
        session['otp']=otp
        dbHandler.insertotp(request)
        msg = mail.send_message(
        'Send Mail tutorial!',
        sender='connectevery1@gmail.com',
        recipients=['anuragt0007@gmail.com'],
        body="Your one time password for this anonymous website is " + str(otp) + " will be valid for lifetime..."
    )

	return redirect(url_for('otp_verify'))
    
    if request.method=='GET':
    	print("inside GET Method")
    	return render_template('registration.html')


######################### otp verify ################################################
@app.route('/otp_verify', methods=['POST', 'GET'])
def otp_verify():
    if request.method=='GET':
        print("inside GET Method")
        return render_template('otp.html')
    if request.method=='POST':
        print("qweret")
        otp=request.form['otp']
        otp_from_db = dbHandler.otp_verification(request)
        print(">>>>>>>>>>>>>>>>>>>>>> " + str(otp))
        print(">>>>>>>>>>>>>>>>>>>>>> " + str(otp_from_db))

        if int(otp_from_db)==int(otp):
            return redirect(url_for('home'))
        else:
            return render_template("otp.html", message="OTP did not match")


######################## logout #################################################
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'mobile' in session:
        name = session.pop('mobile')
        return render_template("result.html", message=name +" has logged out Successfully.")
    
    return render_template("result.html", message="You are already logged out.")


######################### home ################################################
@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method=='POST':
        if dbHandler.insertUser(request):
            msg = "success in adding user"
        else:
            msg = "failed to add user"

	return render_template("otpverify.html", message=msg)
    
    if request.method=='GET':
    	print("inside GET Method of home")
    	if 'mobile' in session :
    		rows = dbHandler.get_images()
    		print rows
        	return render_template("home.html", data = rows)

        else:
    	   return redirect(url_for('login'))

######################## logout #################################################
@app.route('/tweet', methods=['POST', 'GET'])
def tweet():
    if request.method=='GET':
        print("inside GET Method")
        rows = dbHandler.get_tweet()
        print rows
        return render_template("tweet.html", data = rows)

    if request.method=='POST':
        mobile=session['mobile']
        tweet=request.form['tweet']
        date= datetime.date(datetime.now())

        if dbHandler.insertTweet(request):
            print("ho gaya")
            return redirect(url_for('tweet'))


######################## dummy #################################################
@app.route('/dummy', methods=['POST', 'GET'])
def dummy():
    if request.method=='GET':
        return render_template("dummy.html", message="")



######################## NEWS #################################################
@app.route('/headlines/', methods=['POST', 'GET'])
def headlines():
    if request.method=='GET':
        url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=82d1bec56bff4908b7eae0d6f932d3d9')
        response = requests.get(url)
        print(type(response))
        news_article=[]
        news_article = response.json()['articles']
        print(type(news_article))

        return render_template("news.html", data=news_article)

########################   PETROL PRICES #################################################
@app.route('/petrolprices/', methods=['POST', 'GET'])
def petrolprices():
    if request.method=='GET':
        response = unirest.post("https://fuelprice.p.rapidapi.com",
            headers={
            "X-RapidAPI-Key": "a5a37101b0msh05482ff14039b8bp1da28ejsn2a6dc4c6cfbe",
            "Content-Type": "application/x-www-form-urlencoded"})
        print(type(response))
        print(response)

        return render_template("petrolprices.html",data="asd")

########################   PETROL PRICES #################################################
@app.route('/dontknow/', methods=['POST', 'GET'])
def dontknow():
    if request.method=='GET':
        response = unirest.post("https://fuelprice.p.rapidapi.com",
            headers={
            "X-RapidAPI-Key": "a5a37101b0msh05482ff14039b8bp1da28ejsn2a6dc4c6cfbe",
            "Content-Type": "application/x-www-form-urlencoded"})
        print(type(response))
        print(response)

        return render_template("petrolprices.html",data="asd")

@

