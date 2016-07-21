from wtforms import Form, StringField, BooleanField, PasswordField, validators

class RegistrationForm(Form):
	username = StringField('Username', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Password must match')])
	email = StringField('Email', [validators.DataRequired()])
	confirm = PasswordField('Repeat password', [validators.DataRequired()])
	

class LoginForm(Form):
	username = StringField('Username', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])
	rememberme = BooleanField('Remember me', default=False)

