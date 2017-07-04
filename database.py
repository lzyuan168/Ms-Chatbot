import MySQLdb
from config import Config

### function for adding data
def add_data(user_id, reply, entity, value):    

    ### open database connection
    connection = MySQLdb.connect(Config.get_host(), Config.get_user(), Config.get_password(), Config.get_database())

    ### prepare a cursor object using cursor() method
    cursor = connection.cursor()    

    sql = "INSERT INTO user_reply (user_id, reply, entity, value) VALUES (%s, %s, %s, %s)"
    data = (user_id, reply, entity, value) ### prevent SQL Injection
          
    cursor.execute(sql, data) ### execute the SQL command
    connection.commit() ### commit the changes in the database
    cursor.close()
    connection.close() ### disconnect from server
    

#add_data("user_555", "reply message", "entity test", "value test")


### function for reading data
def read_data(user_id):

    ### open database connection
    connection = MySQLdb.connect(Config.get_host(), Config.get_user(), Config.get_password(), Config.get_database())

    ### prepare a cursor object using cursor() method
    cursor = connection.cursor()

    sql = "SELECT * FROM user_reply WHERE user_id = %s"
    data = (user_id,)

    cursor.execute(sql, data) 
    results = cursor.fetchall()
    result_list = []

    for row in results:
        result_list.append(list(row))
    
    
    cursor.close()
    connection.close()

    #print(result_list)
    return result_list

#read_data("user_123")


### function for getting the user last response
def read_last_data(user_id):

    ### open database connection
    connection = MySQLdb.connect(Config.get_host(), Config.get_user(), Config.get_password(), Config.get_database())

    ### prepare a cursor object using cursor() method
    cursor = connection.cursor()
    
    sql = "SELECT * FROM user_reply WHERE user_id = %s ORDER BY id DESC LIMIT 1"
    data = (user_id,)

    cursor.execute(sql, data)
    results = cursor.fetchone()
    result_list = []
    result_list.append(list(results))

    cursor.close()
    connection.close()

    return result_list


#print(read_last_data('1557189344293386'))


### reading data for update
def update_read(user_id, entity):

    ### open database connection
    connection = MySQLdb.connect(Config.get_host(), Config.get_user(), Config.get_password(), Config.get_database())

    ### prepare a cursor object using cursor() method
    cursor = connection.cursor()

    sql = "SELECT * FROM user_reply WHERE user_id = %s AND entity = %s"
    data = (user_id, entity)

    cursor.execute(sql, data)
    results = cursor.fetchone()
    result_list = []
    result_list.append(list(results))

    cursor.close()
    connection.close()

    return result_list



### updating the data in the table
def update_data(user_id, reply_updated, value_updated, reply_original, entity):

    ### open database connection
    connection = MySQLdb.connect(Config.get_host(), Config.get_user(), Config.get_password(), Config.get_database())

    ### prepare a cursor object using cursor() method
    cursor = connection.cursor()

    sql = "UPDATE {}.user_reply SET reply = %s, value = %s WHERE user_id = %s AND reply = %s AND entity = %s".format(Config.get_database())
    data = (reply_updated, value_updated, user_id, reply_original, entity)

    cursor.execute(sql, data)
    connection.commit()
    cursor.close()
    connection.close()

#print("updating...")
#update_data("user_222", "i am going france", "france", "i'm going japan",  "destination")
#update_data("user_444", "new reply", "new value", "reply message",  "entity test")
#print("probably updated")


### delete the selected data in the table
def delete_data(user_id, reply, entity):

    ### open database connection
    connection = MySQLdb.connect(Config.get_host(), Config.get_user(), Config.get_password(), Config.get_database())

    ### prepare a cursor object using cursor() method
    cursor = connection.cursor()

    sql = "DELETE FROM user_reply WHERE user_id = %s AND reply = %s AND entity = %s"
    data = (user_id, reply, entity)

    cursor.execute(sql, data)
    connection.commit()
    cursor.close()
    connection.close()


### delete everything from the table
def delete_all():

    ### open database connection
    connection = MySQLdb.connect(Config.get_host(), Config.get_user(), Config.get_password(), Config.get_database())

    ### prepare a cursor object using cursor() method
    cursor = connection.cursor()

    sql = "DELETE FROM user_reply"

    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


### reset auto increment to 1
def reset_auto_increment():
    ### open database connection
    connection = MySQLdb.connect(Config.get_host(), Config.get_user(), Config.get_password(), Config.get_database())

    ### prepare a cursor object using cursor() method
    cursor = connection.cursor()

    sql = "ALTER TABLE user_reply AUTO_INCREMENT = 1"

    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

