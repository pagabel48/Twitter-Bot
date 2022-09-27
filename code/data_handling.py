from asyncio.windows_events import NULL
from audioop import add
import sqlite3
 
 
class Router():
    def __init__(self, dataBaseName, tableName1, tableName2, connection) -> None:
        self.dataBaseName = dataBaseName
        self.tableName1 = tableName1
        self.tableName2 = tableName2
        self.conn = connection
        self.cur = self.conn.cursor()

    def duplicate(self, table, field, value):
        self.cur.execute('SELECT id FROM %s WHERE %s = "%s"' %(table, field, value, ))
        data = self.cur.fetchall()
        if (len(data) == 0):
            return False
        else:
            return True
 
    # add user to database
    def addAccountToDatabase(self, userId, username, name, tweets, followers, following, location, likes, verified): #first parameter is string, rest are integers
        #if all data fields are filled out and data is not a duplicate then populate the database with the user
        if(bool(userId) == bool(username) == True and not self.duplicate(self.tableName1, "username", username)):
            #change datatype of an input
            if(verified):
                self.isVerified = 1
            elif(not verified):
                self.isVerified ==0
            else:
                #potential error case
                print("Improper verification value passed.")
                exit()
            print(userId)
            print(username)
            print(name)
            print(tweets)
            print(followers)
            print(following)
            print(location)
            print(likes)
            print(self.isVerified)

            #try:
            self.cur.execute('''
                    INSERT INTO ''' + self.tableName1 + ''' (userId, username, name, numberOfFollowers, numberOfFollowing, numberOfTweets, location, likes, verified, used)
                        VALUES(''' + str(userId) + ''', "''' + username + '''", "''' + name + '''", ''' + str(followers) + ''', ''' + str(following) + ''', ''' + str(tweets) + ''', "''' + location + '''", '''  + str(likes) + ''', ''' + str(self.isVerified) + ''', 0);
                ''')
            self.conn.commit()
            #except:
            #    print("an error occured")
        else:
            print("invalid null variable attribute")

    def addHashtagToDatabase(self, hashtag):
        if(bool(hashtag) and not self.duplicate(self.tableName2, "hashtag", hashtag)):
                self.cur.execute('''
                    INSERT INTO ''' + self.tableName2 + '''(hashtag, used)
                        VALUES("''' + hashtag +''', 0);
                ''')
        else:
            print("Missing Data")
 
    #change status of an account (so it isn't read again)
    def setValueRead(self, table, Id):
        self.cur.execute("UPDATE " + table + " SET used = 1 WHERE id = " + str(Id))
        self.conn.commit()
 
    def getUsernameFromDatabase(self):
        selectionCommand = "SELECT id, username FROM %s WHERE used = 0" %(self.tableName1,)
 
        self.cur.execute(selectionCommand)
        data = self.cur.fetchone()
        if(data):
            print(data[0])
            self.setValueRead(self.tableName1, data[0])
            return(data[1])
        else:
            print("no available accounts to read")
 
    def finish(self):
        self.conn.close()
        print("All Done")
 
    def getDatabaseRows(self):
        self.cur.excecute("COUNT(*) FROM " + self.tableName)
 
#databaseName = "Accounts.db"
#accountName = "Accounts"
#databaseConnection = sqlite3.connect(databaseName)
 
#datum = dataHandling(databaseName, accountName, databaseConnection)
#print(datum.getAccountFromDatabase())
#datum.finish()
 
#sessionId = "AYcsw19lx4e8LZqwrEbgmY0jkWtEkBK5KrrJI2ZI8w"
#user = InstagramHashTag('mahsaamini', sessionid = sessionId)
#print(user.number_of_posts)
