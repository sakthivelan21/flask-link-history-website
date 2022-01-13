'''
importing the flask and its libraries

Flask = core of the server

render_template = to render the html pages for request

url_for = to map the path in html templates

redirect = to cause the pages to redirect to new routes

request = to handle the data passed in request from forms

'''

from flask import Flask,render_template,url_for,request,redirect

'''
importing the SQLAlchemy libraries for connecting to the database 
'''

from flask_sqlalchemy import SQLAlchemy

# for date and time usage 
from datetime import datetime

# setting the flask class as app
app=Flask(__name__)

'''
configuring the database file path to the server

we are using sqlite as the database
'''

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

# setting the database lines through SQLAlchemy for convenient use
db=SQLAlchemy(app)

# create a table model which will create and give a hold on the table in the database file
class DataModel(db.Model):
	
	id=db.Column(db.Integer,primary_key=True)
	
	name=db.Column(db.String(200),nullable=False)
	
	url=db.Column(db.String(200),nullable=False)
	
	date_created=db.Column(db.DateTime,default=datetime.utcnow)
	
	def __repr__(self):
	
		return 'Link %r' % self.id

# home route 
@app.route("/")
def homeRoute():
	links=DataModel.query.order_by(DataModel.date_created).all()
	return render_template("index.html",links=links)		

# addLink route to add link data into the table			
@app.route("/addLink",methods=['POST'])
def addLink():
	if request.method=='POST':
		link_name=request.form['name']
		link_url=request.form['url']
		dataModel=DataModel(name=link_name,url=link_url)
		try:
			db.session.add(dataModel)
			db.session.commit()
			return redirect('/')	
		except:
			return "error occured in data insertion point"
	else:
		return redirect('/')

# updateLink route to provide update page
@app.route("/updateLink/<int:id>")
def updateLinkPage(id):
	link=DataModel.query.get_or_404(id)
	return render_template("update.html",link=link)	

# updateLink data to update the values in the table
@app.route("/updateLinkData/<int:id>",methods=['POST'])
def updateLinkData(id):
	link=DataModel.query.get_or_404(id)
	link.name=request.form['name']
	link.url=request.form['url']
	try:
		db.session.commit()
		return redirect('/')
	except:
		"There was an error occured in updating"

# deleteLink to remove the data from the table
@app.route("/deleteLink/<int:id>")
def deleteLink(id):
	link_to_be_deleted=DataModel.query.get_or_404(id)
	try:
		db.session.delete(link_to_be_deleted)
		db.session.commit()
		return redirect('/')
	except:
		"There was an error occured in deletion"

# to start the server in debug mode
if __name__=="__main__":
	app.run(debug=True)
	
