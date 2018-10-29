import mysql.connector

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
    mycursor.execute("CREATE DATABASE " + dbName)

try:
    myDB = mysql.connector.connect(
        host="localhost",
        user="possegger",
        passwd="P@ssw0rd$!"
    )
    mycursor = myDB.cursor()
    #CreateDB
    createDB(mycursor, "testDB")
    
except Exception as x:
    print(x)