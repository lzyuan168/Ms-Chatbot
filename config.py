import os

#os.environ["DATABASE_NAME"] = "test"
class Config():	

	def get_host():
		os.environ["DB_HOST"] = "localhost"
		return os.environ["DB_HOST"]

	def get_user():
		os.environ["DB_USER"] = "root"
		return os.environ["DB_USER"]

	def get_password():
		os.environ["DB_PASSWORD"] = "root"
		return os.environ["DB_PASSWORD"]

	def get_database():
		database = os.environ.get("DATABASE_NAME", "insurance_test")
		return database


#print(Config.get_database())