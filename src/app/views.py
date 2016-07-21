from flask import render_template, request, flash, redirect, url_for
from app import app
from .forms import RegistrationForm, LoginForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/volunteers')
def volunteers():
	return render_template('get_volunteers_list.html')

@app.route('/volunteers/<volunteer_id>')
def volunteer(volunteer_id):
	return render_template('get_volunteer_infos.html', volunteer_id=volunteer_id)

@app.route('/gardens')
def gardens():
	return render_template('get_gardens_list.html')

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
		flash('Thanks for registering!')
		return redirect(url_for('login'))
	return render_template('register.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		password = form.password.data
		flash('You\'re now logged in!')
		return redirect(url_for('index'))
	return render_template('login.html', form=form)
