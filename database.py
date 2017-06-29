import MySQLdb

host = "localhost"
user = "root"
password = "root"
database = "insurance"
database_test = "insurance_test"


### function for adding data
def add_data(user_id, reply, entity, value, *args):    

    ### open database connection
    if "test":
        connection = MySQLdb.connect(host, user, password, database_test)
    else:
        connection = MySQLdb.connect(host, user, password, database)

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
    connection = MySQLdb.connect(host, user, password, database)

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

#read_data("1557189344293386")


### function for getting the user last response
def read_last_data(user_id):

    ### open database connection
    connection = MySQLdb.connect(host, user, password, database)

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
    connection = MySQLdb.connect(host, user, password, database)

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

    ### open database connecion
    connection = MySQLdb.connect(host, user, password, database)

    ### prepare a cursor object using cursor() method
    cursor = connection.cursor()

    sql = "UPDATE insurance.user_reply SET reply = %s, value = %s WHERE user_id = %s AND reply = %s AND entity = %s" 
    data = (reply_updated, value_updated, user_id, reply_original, entity)

    cursor.execute(sql, data)
    connection.commit()
    cursor.close()
    connection.close()

#print("updating...")
#update_data("user_222", "i am going france", "france", "i'm going japan",  "destination")
#update_data("user_444", "new reply", "new value", "reply message",  "entity test")
#print("probably updated")


### delete the data in the table
def delete_data(user_id, reply, entity):

    ### open database connection
    connection = MySQLdb.connect(host, user, password, database)

    ### prepare a cursor object using cursor() method
    cursor = connection.cursor()

    sql = "DELETE FROM user_reply WHERE reply = %s AND entity = %s"
    data = (reply, entity)

    cursor.execute(sql, data)
    connection.commit()
    cursor.close()
    connection.close()
