#!/usr/bin/python3
import mysql.connector

'''
def getDBs(mycursor): #Return all dbs
    dbArray = []
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        dbArray.append(x)
    return dbArray
        

def createDB(mycursor, dbName): #Creates DB if it does not already exists
    for x in getDBs(mycursor):
        if x == dbName:
            return
    mycursor.execute(f'CREATE DATABASE {dbName}') #F is the python string builder
'''
myDB = None #Same as null

try:
    myDB = mysql.connector.connect(
        host="localhost",
        #user="possegger",
        #passwd="P@ssw0rd$!"
        user="simon",
        passwd="P@ssw0rd$!-278",
        database="attendid"
    )
    mycursor = myDB.cursor()
    #CreateDB if not already exists
    #createDB(mycursor, 'attendID')

    #Create Table
    #mycursor.execute("CREATE TABLE attendingStudents (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
    
    #Insert into table
    sql_query = (f"INSERT INTO attendingStudents (TimeStamp,Class,AttendingStudents) VALUE (%s,%s,%s)")
    sql_value = ("2018-11-05 11:31:00","4AHITN", 0)
    mycursor.execute(sql_query,sql_value)
    #Commit changes
    myDB.commit()
    print('Changes commited')

except Exception as x:
    print(x)

finally:
    if myDB:
        myDB.close()
