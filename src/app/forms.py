from wtforms import Form, SubmitField, StringField, BooleanField, PasswordField, SelectField, HiddenField, validators

class RegistrationForm(Form):
	username = StringField('Username', [validators.DataRequired(), validators.Length(min=6, max=25, message='Username must have at least 6 characters and maximum 25.')])
	password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Password must match')])
	email = StringField('Email', [validators.DataRequired(), validators.Email()])
	confirm = PasswordField('Repeat password', [validators.DataRequired()])
	
class LoginForm(Form):
	username = StringField('Username', [validators.DataRequired(), validators.Length(min=6, max=25, message='Username must have at least 6 characters and maximum 25.')])
	password = PasswordField('Password', [validators.DataRequired()])
	rememberme = BooleanField('Remember me', default=False)

class AddTaskForm(Form):
	gardenname = SelectField('Gardens list', coerce=int)
	task = StringField('Task', [validators.DataRequired()])
	addtask = SubmitField('Add task')

class DeleteTaskForm(Form):
	taskid = HiddenField('taskid')
	edittask = SubmitField('Edit')
	deletetask = SubmitField('Delete')

class UpdateTaskForm(Form):
	garden = StringField('Garden')
	task = StringField('Task', [validators.DataRequired()])
	save = SubmitField('Save')

class AddGardenForm(Form):
	name = StringField('name', [validators.DataRequired()])
	category = SelectField('Categories list', coerce=int)
	address = StringField('Address', [validators.DataRequired()])
	submit = SubmitField('Create')