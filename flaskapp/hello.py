from flask import Flask
from flask import render_template
import models as dbHandler
from flask import request

from flask import session

app = Flask(__name__ )

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
	print("something")
	if 'username' in session:
		return render_template("result.html", message=session['username'] +" has already logged in,  first logout!!!")
	elif request.method == 'POST':
		if dbHandler.authenticate(request):
			session['username'] = request.form['username']
			msg = "successful login" 
		else:
			msg ="login failed"

		return render_template("result.html", message=msg)

	return render_template('login.html')



######################### register ################################################
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        if dbHandler.insertUser(request):
            msg = "success in adding user"
        else:
            msg = "failed to add user"

	return render_template("result.html", message=msg)
    
    if request.method=='GET':
    	return render_template('registration.html')