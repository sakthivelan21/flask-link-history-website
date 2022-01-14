'''
importing the flask and its libraries

Flask = core of the server

render_template = to render the html pages for request

url_for = to map the path in html templates

redirect = to cause the pages to redirect to new routes

request = to handle the data passed in request from forms

'''

from flask import Flask,render_template,url_for,request,redirect,g,session

'''
importing the SQLAlchemy libraries for connecting to the database 
'''

from flask_sqlalchemy import SQLAlchemy

# for date and time usage 
from datetime import datetime

# for safely storing password and checking them
from werkzeug.security import generate_password_hash,  check_password_hash

import functools

# setting the flask class as app
app=Flask(__name__)

'''
configuring the database file path to the server

we are using sqlite as the database
'''

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#config the session to the app
app.secret_key='secretkeyisverysecret'

# setting the database lines through SQLAlchemy for convenient use
db=SQLAlchemy(app)


# table model for user database

class UserModel(db.Model):
	
	id=db.Column(db.Integer,primary_key=True)
	
	name=db.Column(db.String(100),nullable=False)
	
	user_id=db.Column(db.String(100),nullable=False)
	
	password=db.Column(db.String(100),nullable=False)
	
	dataModel=db.relationship('DataModel',backref="user_model")
	
	def __repr__(self):
		
		return 'Link  %r' % self.id

# create a table model which will create and give a hold on the table in the database file
class DataModel(db.Model):
	
	id=db.Column(db.Integer,primary_key=True)
	
	name=db.Column(db.String(200),nullable=False)
	
	url=db.Column(db.String(200),nullable=False)
	
	date_created=db.Column(db.DateTime,default=datetime.utcnow)
	
	user_id=db.Column(db.Integer,db.ForeignKey('user_model.id'))
	
	def __repr__(self):
	
		return 'Link %r' % self.id

#setting the app route with @ and routing the pages with function to do what we want with the route
@app.before_request
def before_request():
    user_id=session.get('user_id')
    if user_id is None:
        g.user=None
    else:
        g.user=user_id

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect('/')

        return view(**kwargs)

    return wrapped_view
    

# home page route 

@app.route("/home")
@login_required
def homePage():
	links=DataModel.query.filter(DataModel.user_id==g.user).order_by(DataModel.date_created).all()
	return render_template("home.html",links=links)	

# updateLink route to provide update page
@app.route("/updateLink/<int:id>")
@login_required
def updateLinkPage(id):
	link=DataModel.query.get_or_404(id)
	return render_template("update.html",link=link)	

# login page route	
@app.route("/")
def loginPage():
	return render_template("login.html",error="")	

# signup page route
@app.route("/signup")
def signupPage():
	return render_template("signup.html",error="")

@app.route("/authenticate-user",methods=['POST'])
def login_user():
	error=""
	if request.method=='POST':
		user_id=request.form['userId']
		user_password=request.form['password']
		
		user_finded=UserModel.query.filter(UserModel.user_id==user_id).first()
		if user_finded==None:
			error="invalid user name !!!"
		else:
			if check_password_hash(user_finded.password,user_password):
				session['user_id']=user_finded.id
				print(str(session['user_id'])+"session created !!!")
				return redirect("/home")
			else:
				error="invalid password !!"
			
	return render_template("login.html",error=error)

# signup post request for saving the user to db
@app.route("/signup-user",methods=['POST'])
def signup_user():
	error=""
	if request.method=='POST':
		user_name=request.form['name']
		user_id=request.form['userId']
		user_password=request.form['password']
		user=UserModel.query.filter(UserModel.user_id==user_id).first()
		print(user)
		if bool(user):
			error="user_id already exists !! try giving a new unique user id !!"	
		else:
			userModel=UserModel(name=user_name,user_id=user_id,password=generate_password_hash(user_password))
			try:
				db.session.add(userModel)
				db.session.commit()
				session['user_id']=UserModel.query.filter(UserModel.user_id==user_id).first().id
				print(str(session['user_id'])+"session created !!!")
				return redirect('/home')
			except:
				error="error occured while registering user try again please !!"
	return render_template("signup.html",error=error)

# addLink route to add link data into the table			
@app.route("/addLink",methods=['POST'])
@login_required
def addLink():
	if request.method=='POST':
		link_name=request.form['name']
		link_url=request.form['url']
		dataModel=DataModel(name=link_name,url=link_url,user_id=g.user)
		try:
			db.session.add(dataModel)
			db.session.commit()
			return redirect('/home')	
		except:
			return "error occured in data insertion point"
	else:
		return redirect('/home')

# updateLink data to update the values in the table
@app.route("/updateLinkData/<int:id>",methods=['POST'])
@login_required
def updateLinkData(id):
	link=DataModel.query.get_or_404(id)
	link.name=request.form['name']
	link.url=request.form['url']
	try:
		db.session.commit()
		return redirect('/home')
	except:
		"There was an error occured in updating"

# deleteLink to remove the data from the table
@app.route("/deleteLink/<int:id>")
@login_required
def deleteLink(id):
	link_to_be_deleted=DataModel.query.get_or_404(id)
	try:
		db.session.delete(link_to_be_deleted)
		db.session.commit()
		return redirect('/home')
	except:
		"There was an error occured in deletion"

@app.route('/sign_out',methods=['POST'])
@login_required
def sign_out():
    if request.method=='POST':
    	print(str(session['user_id']) +"session cleared")
    	g.user=None
    	session.clear()
    return redirect('/')
   
# to start the server in debug mode
if __name__=="__main__":
	app.run(debug=True)
	
