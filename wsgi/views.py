from app import app , db , login_manager
from flask import render_template , request , flash , redirect , url_for ,g , jsonify , Response
from models import Users
from flask.ext.login import login_user , logout_user , current_user , login_required
from bson.objectid import ObjectId
import json
from bson import json_util
from datetime import datetime
from pygeocoder import Geocoder

@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def index():
	return render_template('index.html',title="Welcome to LocalJobs -- Location Aware Job Search Application")

@login_manager.user_loader
def load_user(id):
	users_dict = db.users.find_one({"_id": ObjectId(str(id))})
	registered_user = Users(users_dict.get('email'),users_dict.get('password'),users_dict.get('linkedin_profile_url'),users_dict.get('skills'))
	registered_user.id = users_dict.get('_id')
	return registered_user


@app.route('/about')
def about():
	return render_template('about.html',title="About LocalJobs")


@app.route('/contact')
def contact():
	return render_template('contact.html' , title="Contact Us")

@app.route('/signin' , methods=['GET','POST'])
def signin():
	if request.method == 'GET':
		return render_template('signin.html' , title="Signin to LocalJobs")

	email = request.form['email']
	password = request.form['password']
	remember_me = False
	if 'rememberme' in request.form:
		remember_me = True
	users_dict = db.users.find_one({'email':email , 'password':password})
	if users_dict is None:
		flash('Email or password is invalid' , 'error')
		return redirect(url_for('signin'))
	registered_user = Users(users_dict.get('email'),users_dict.get('password'),users_dict.get('linkedin_profile_url'),users_dict.get('skills'))
	registered_user.id = users_dict.get('_id')
	login_user(registered_user, remember = remember_me)
	flash('Logged in successfully')
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/register' , methods=['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html' , title="Register for LocalJobs Account")
	email = request.form['email']
	if db.users.find_one({'email':email}):
		flash('User exist with email id %s' % email,'error')
		return redirect(url_for('register'))
	skills = [skill.strip().lower() for skill in request.form['skills'].split(',')]
	user = Users(request.form['email'],request.form['password'],request.form['linkedinUrl'],skills)
	user_id = db.users.insert(user.__dict__ , w=1)
	flash(u'User created with id %s' % user_id)
	return redirect(url_for('signin'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 


@app.route('/jobs/new' , methods=['GET'])
@login_required
def job_form():
	return render_template('job.html' , title="Create New Job")

@app.route('/jobs/new' , methods=['POST'])
@login_required
def create_job():
	title = request.form['title']
	description = request.form['description']
	skills = [skill.strip().lower() for skill in request.form['skills'].split(',')]
	location = request.form['location']
	createdOn = datetime.utcnow()
	companyName = request.form["companyName"]
	companyWebSite = request.form["companyWebsite"]
	companyContactEmail = request.form["companyContactEmail"]
	companyContactTelephone = request.form["companyContactTelephone"]
	results = Geocoder.geocode(location)
	lngLat = [results[0].coordinates[1],results[0].coordinates[0]]

	job = {
		"title" : title,
		"description" : description,
		"skills" : skills,
		"location" : location,
		"lngLat" : lngLat,
		"createdOn" : createdOn,
		"company" : {
			"name" : companyName,
			"website" : companyWebSite,
			"contact" :{
				"email": companyContactEmail,
				"telephone" : companyContactTelephone
			}
		}
	}
	job_id = db.jobs.insert(job , w=1)
	flash(u'Job created with id %s' % job_id)
	return redirect(url_for('create_job'))

@app.route('/jobs/search')
@login_required
def search():
	return render_template('search.html' , title="Search Jobs")

@app.route('/api/jobs/<skills>')
@login_required
def jobs_near_with_skills(skills):
	lat = float(request.args.get('lat'))
	lon = float(request.args.get('lng'))

	results = db.jobs.find({"skills" : {"$in" : skills.split(',')} , "lngLat" : { "$near" : [lon,lat]}}).limit(5)
	jobs = []
	for result in results:
		jobs.append(result)

	return json_response(jobs)

@app.route('/api/jobs')
@login_required
def jobs():
	jobs = db.jobs.find().limit(25)
	return json.dumps({'jobs':list(jobs)},default=json_util.default)

@app.route('/api/jobs/id/<job_id>')
@login_required
def job(job_id):
	job = db.jobs.find_one({"_id":ObjectId(str(job_id))})
	return json.dumps({'job':job},default=json_util.default)

def json_response(data):
	return Response(json.dumps({'jobs':data},default=json_util.default),mimetype="application/json")