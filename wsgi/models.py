class Users(object):
	id = None
	def __init__(self , email , password , linkedin_profile_url , skills):
		
		self.email = email
		self.password = password
		self.linkedin_profile_url = linkedin_profile_url
		self.skills = skills

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)