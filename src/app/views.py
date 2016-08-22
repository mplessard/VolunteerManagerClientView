from flask import render_template, request, flash, redirect, url_for, session
from app import app
from .forms import RegistrationForm, LoginForm, AddTaskForm, DeleteTaskForm, UpdateTaskForm, AddGardenForm
import requests, json, urllib

esb_url = 'http://localhost:8280/manager/api/'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		session.pop('token', None)
	return render_template('index.html')

@app.route('/volunteers')
def volunteers():
	volunteers_list = get_json(esb_url + 'volunteers?access_token=' + session['token'])
	return render_template('get_volunteers_list.html', volunteers_list=volunteers_list)

@app.route('/volunteers/<volunteer_id>', methods=['GET', 'POST'])
def volunteer(volunteer_id):
	form = [AddTaskForm(request.form), DeleteTaskForm(request.form)]
	gardens_list = get_json(esb_url + 'gardens?access_token=' + session['token'])
	form[0].gardenname.choices = [(gn['id'], gn['name']) for gn in gardens_list['gardens']]
	
	if request.method == 'POST' and form[0].validate():
		gardenname = form[0].gardenname.data
		task = form[0].task.data

		r = requests.post(esb_url + 'volunteers/' + str(volunteer_id) + '/tasks?access_token=' + session['token'],
			data={'gardenid': gardenname, 'task': task})
		flash(r.text)

	volunteer_infos = get_json(esb_url + 'volunteers/' + str(volunteer_id) + '?access_token=' + session['token'])
	return render_template('get_volunteer_infos.html', volunteer_id=volunteer_id, form=form, volunteer_infos=volunteer_infos, esb_url=esb_url)

@app.route('/volunteers/<volunteer_id>/update/tasks/<task_id>', methods=['GET', 'POST'])
def updateTask(volunteer_id, task_id):
	task_infos = get_json(esb_url + 'volunteers/' + str(volunteer_id) + '/tasks/' + str(task_id) + '?access_token=' + session['token'])
	gardens = get_json(esb_url + 'gardens/' + str(task_infos['gardenID']) + '?access_token=sVmThUIdLblP1oVOvDB6eHpBIollsO3NNmuSq-dOrlCsYZWMmRVhI8i_aXTyzQIB')
	form = UpdateTaskForm(request.form)

	if request.method == 'POST' and form.validate():
		taskdesc = form.task.data
		r = requests.post(esb_url + 'volunteers/' + str(volunteer_id) + '/tasks/' + str(task_id) + '?access_token=' + session['token'],
			data={'taskdesc': taskdesc})
		flash(r.text)
		return redirect(url_for('volunteer', volunteer_id=volunteer_id))
	return render_template('task_edition.html', volunteer_id=volunteer_id, form=form, task_infos=task_infos, gardens=gardens)

@app.route('/volunteers/<volunteer_id>/delete/tasks/<task_id>', methods=['GET', 'POST'])
def deleteTask(volunteer_id, task_id):
	r = requests.delete(esb_url + 'volunteers/' + str(volunteer_id) + '/tasks/' + str(task_id) + '?access_token=' + session['token'])
	flash(r.text)
	return redirect(url_for('volunteer', volunteer_id=volunteer_id))

@app.route('/gardens')
def gardens():
	gardens_list = get_json(esb_url + 'gardens?access_token=sVmThUIdLblP1oVOvDB6eHpBIollsO3NNmuSq-dOrlCsYZWMmRVhI8i_aXTyzQIB')
	return render_template('get_gardens_list.html', gardens_list=gardens_list)

@app.route('/gardens/<garden_id>')
def garden(garden_id):
	garden_infos = get_json(esb_url + 'gardens/' + str(garden_id) + '?access_token=sVmThUIdLblP1oVOvDB6eHpBIollsO3NNmuSq-dOrlCsYZWMmRVhI8i_aXTyzQIB')
	return render_template('get_garden_infos.html', garden_id=garden_id, garden_infos=garden_infos)

@app.route('/add/garden', methods=['GET', 'POST'])
def addGarden():
	form = AddGardenForm(request.form)
	categories = get_json(esb_url + 'gardens/categories?access_token=' + session['token'])
	form.category.choices = [(c['id'], c['name']) for c in categories['categories']]

	if request.method == 'POST' and form.validate():
		name = form.name.data
		category = form.category.data
		address = form.address.data

		r = requests.post(esb_url + 'gardens?access_token=' + session['token'],
			data={'name': name, 'category': category, 'address': address})
		flash(r.text)
		return redirect(url_for('gardens'))
	return render_template('add_garden.html', form=form)

@app.route('/delete/garden/<garden_id>')
def deleteGarden(garden_id):
	r = requests.delete(esb_url + 'gardens/' + str(garden_id) + '?access_token=' + session['token'])
	flash(r.text)

	tasks = get_json(esb_url + 'volunteers/tasks' + '?access_token=' + session['token'])

	for t in tasks:
		if t['gardenID'] == int(garden_id):
		 	r = requests.delete(esb_url + 'volunteers/' + str(t['volunteerID']) + '/tasks/' + str(t['taskID']) + '?access_token=' + session['token'])

	return redirect(url_for('gardens'))

@app.route('/update/garden/<garden_id>', methods=['GET', 'POST'])
def updateGarden(garden_id):
	form = AddGardenForm(request.form)
	categories = get_json(esb_url + 'gardens/categories?access_token=' + session['token'])
	form.category.choices = [(c['id'], c['name']) for c in categories['categories']]
	garden_infos = get_json(esb_url + 'gardens/' + garden_id + '?access_token=' + session['token'])

	if request.method == 'POST' and form.validate():
		name = form.name.data
		category = form.category.data
		address = form.address.data

		r = requests.post(esb_url + 'gardens/' + str(garden_id) + '?access_token=' + session['token'],
			data={'name': name, 'category': category, 'address': address})
		flash(r.text)
		return redirect(url_for('gardens'))
	return render_template('update_garden.html', form=form, garden_id=garden_id, garden_infos=garden_infos)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		email = form.email.data
		password = form.password.data
		
		r = requests.post(esb_url + 'volunteers',
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
			session['role'] = token_infos['role']
			session['id'] = token_infos['id']

			r2 = requests.post(esb_url + 'gardens/authenticate',
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
