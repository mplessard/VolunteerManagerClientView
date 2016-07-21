from app import db

class MyTestTable(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	myTestField = db.Column(db.String(64), index=True, unique=True)

	def __repr__(self):
		return '<MyTestTable %r>' % (self.myTestField)