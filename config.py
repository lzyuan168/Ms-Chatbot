import os

""" config the database connection """
class Config():	
    
    ### if HOST_NAME is set, return HOST_NAME, else return default value localhost
	def get_host():
		return os.environ.get("HOST_NAME", "localhost")
    
    ### if USER_NAME is set, return USER_NAME, else return default value root
	def get_user():
		return os.environ.get("USER_NAME", "root")
    
    ### if PASSWORD_NAME is set, return PASSWORD_NAME, else return default value root
	def get_password():
		return os.environ.get("PASSWORD_NAME", "root")
    
    ### if DATABASE_NAME is set, return DATABASE_NAME, else return default value insurance_test
	def get_database():
		return os.environ.get("DATABASE_NAME", "insurance_test")


#print(Config.get_database())