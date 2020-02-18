from app import db



class User(db.Model):
	__tablename__= "users"


	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	username = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String)
	role = db.Column(db.String)

	@property
	def is_autenticated(self):
		return True
	@property
	def is_active(self):
		return True

	@property
	def is_anonimous(self):
		return False

	def get_id(self):
		return str(self.id)


	def __init__(self, name, username, email, password, role):
		self.name = name
		self.username = username
		self.email = email
		self.password = password
		self.role = role

	def __repr__(self):
		return "<User %r>" % self.username


class Post(db.Model):
	__tablename__ = "posts"


	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	description = db.Column(db.Text)
	content = db.Column(db.Text)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

	user = db.relationship('User', foreign_keys=user_id)

	def __init__(self, title, description, content, created_at, updated_at, user_id):
		self.title = title
		self.description = description
		self.content = content
		self.created_at = created_at
		self.updated_at = created_at
		self.user_id = user_id

	def __repr__(self):
		return '<Post %r>' % self.id


class Follow(db.Model):
	__tablename__ = "follow"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	follower_id = db .Column(db.Integer, db.ForeignKey('users.id'))

	user = db.relationship('User', foreign_keys=user_id)



class CatsTags(db.Model):
	__tablename__ = "catstags"

	id = db.Column(db.Integer, primary_key=True)
	catag_name = db.Column(db.Text)

	catag_parent_id = db .Column(db.Integer, db.ForeignKey('catstags.id'))
	
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('User', foreign_keys=user_id)


class ZipperPostsCatsTags(db.Model):
	__tablename__ = "zipper_posts_catstags"

	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	catag_id = db .Column(db.Integer, db.ForeignKey('catstags.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	#user = db.relationship('User', foreign_keys=user_id)
	#post = db.relationship('Post', foreign_keys=post_id)
	#cattag = db.relationship('CatsTags', foreign_keys=post_id)


	


