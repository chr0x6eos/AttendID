import mysql.connector

def showDBs(mycursor):
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        print(x)

try:
    myDB = mysql.connector.connect(
        host="localhost",
        user="possegger",
        passwd="P@ssw0rd$!"
    )
    mycursor = myDB.cursor()
    #print("Before creating")
    #showDBs(mycursor)
    mycursor.execute("CREATE DATABASE testDB")
    #print("After creating")
    #showDBs(mycursor)
except:
    print("Error")