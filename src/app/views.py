from flask import render_template, request, flash, redirect, url_for, session
from app import app
from .forms import RegistrationForm, LoginForm, AddTaskForm, DeleteTaskForm, UpdateTaskForm, AddGardenForm
import requests, json, urllib

appendGardenUrl = 'http://localhost:8081/GardenManager/api/v1/gardenservice/'
appendVolunteerUrl = 'http://localhost:8080/VolunteerManager/api/v1/volunteerservice/'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		session.pop('token', None)
	return render_template('index.html')

@app.route('/volunteers')
def volunteers():
	return render_template('get_volunteers_list.html')

@app.route('/volunteers/<volunteer_id>', methods=['GET', 'POST'])
def volunteer(volunteer_id):
	form = [AddTaskForm(request.form), DeleteTaskForm(request.form)]
	gardens_list = get_json(appendGardenUrl + 'gardens?access_token=' + session['token'])
	form[0].gardenname.choices = [(gn['id'], gn['name']) for gn in gardens_list['gardens']]
	
	if request.method == 'POST' and form[0].validate():
		gardenname = form[0].gardenname.data
		task = form[0].task.data

		r = requests.post(appendVolunteerUrl + 'volunteers/' + str(volunteer_id) + '/tasks?access_token=' + session['token'],
			data={'gardenid': gardenname, 'task': task})
		flash(r.text)
	return render_template('get_volunteer_infos.html', volunteer_id=volunteer_id, form=form)

@app.route('/volunteers/<volunteer_id>/update/tasks/<task_id>', methods=['GET', 'POST'])
def updateTask(volunteer_id, task_id):
	form = UpdateTaskForm(request.form)

	if request.method == 'POST' and form.validate():
		taskdesc = form.task.data
		r = requests.post(appendVolunteerUrl + 'volunteers/' + str(volunteer_id) + '/tasks/' + str(task_id) + '?access_token=' + session['token'],
			data={'taskdesc': taskdesc})
		flash(r.text)
		return redirect(url_for('volunteer', volunteer_id=volunteer_id))
	return render_template('task_edition.html', volunteer_id=volunteer_id, task_id=task_id, form=form)

@app.route('/volunteers/<volunteer_id>/delete/tasks/<task_id>', methods=['GET', 'POST'])
def deleteTask(volunteer_id, task_id):
	r = requests.delete(appendVolunteerUrl + 'volunteers/' + str(volunteer_id) + '/tasks/' + str(task_id) + '?access_token=' + session['token'])
	flash(r.text)
	return redirect(url_for('volunteer', volunteer_id=volunteer_id))

@app.route('/gardens')
def gardens():
	return render_template('get_gardens_list.html')

@app.route('/add/garden', methods=['GET', 'POST'])
def addGarden():
	form = AddGardenForm(request.form)
	categories = get_json(appendGardenUrl + 'categories?access_token=' + session['token'])
	form.category.choices = [(c['id'], c['name']) for c in categories['categories']]

	if request.method == 'POST' and form.validate():
		name = form.name.data
		category = form.category.data
		address = form.address.data

		r = requests.post(appendGardenUrl + 'gardens?access_token=' + session['token'],
			data={'name': name, 'category': category, 'address': address})
		flash(r.text)
		return redirect(url_for('gardens'))
	return render_template('add_garden.html', form=form)

@app.route('/delete/garden/<garden_id>')
def deleteGarden(garden_id):
	r = requests.delete(appendGardenUrl + 'gardens/' + str(garden_id) + '?access_token=' + session['token'])
	flash(r.text)
	return redirect(url_for('gardens'))

@app.route('/update/garden/<garden_id>', methods=['GET', 'POST'])
def updateGarden(garden_id):
	form = AddGardenForm(request.form)
	categories = get_json(appendGardenUrl + 'categories?access_token=' + session['token'])
	form.category.choices = [(c['id'], c['name']) for c in categories['categories']]

	if request.method == 'POST' and form.validate():
		name = form.name.data
		category = form.category.data
		address = form.address.data

		r = requests.post(appendGardenUrl + 'gardens/' + str(garden_id) + '?access_token=' + session['token'],
			data={'name': name, 'category': category, 'address': address})
		flash(r.text)
		return redirect(url_for('gardens'))
	return render_template('update_garden.html', form=form, garden_id=garden_id)

@app.route('/gardens/<garden_id>')
def garden(garden_id):
	return render_template('get_garden_infos.html', garden_id=garden_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		email = form.email.data
		password = form.password.data
		
		r = requests.post(appendVolunteerUrl + 'volunteers',
			data={'username': username, 'email': email, 'password': password})
		
		if r.status_code == 200:
			flash('Thanks for registering!')
			return redirect(url_for('login'))
		else:
			flash('An error has occurred! ' + str(r.text))
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		password = form.password.data

		r = requests.post('http://localhost:8080/VolunteerManager/api/authentication',
			data={'username': username, 'password': password})

		if r.status_code == 200:
			token_infos = r.json()
			token = token_infos['token']
			exp_date = token_infos['exp_date']
			session['token'] = token
			session['exp_date'] = exp_date
			session['username'] = username

			r2 = requests.post(appendGardenUrl + 'users',
			 	data={'token': token, 'date': exp_date})

			if r2.status_code == 200:
				flash('You\'ve been successfully logged in!')
			return redirect(url_for('index'))
		else:
			flash('An error has occured! Wrong username or password.' + str(r.status_code))
	return render_template('login.html', form=form)

def get_json(link):
	with urllib.request.urlopen(link) as url:
		myfile = url.read().decode('utf8')
	return json.loads(myfile)

app.jinja_env.globals.update(get_json=get_json)
