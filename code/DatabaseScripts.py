import sqlite3
 
DatabaseName = "Accounts"
 
def connectToDataBase(name):
    conn = sqlite3.connect(name + ".db")
 
    return conn
 
def createAccountsDatabase():
    conn = connectToDataBase(DatabaseName)
    conn.execute('''
        CREATE TABLE %s
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER NOT NULL,
            username TEXT NOT NULL,
            name TEXT,
            numberOfFollowers INT,
            numberOfFollowing INT,
            numberOfTweets INT,
            location TEXT,
            likes INT,
            verified INT,
            used INT  
        );''' %("Accounts",))
    print("created Accounts table")

def createHashtagDatabase():
    con = connectToDataBase(DatabaseName)
    con.execute('''
        CREATE TABLE %s
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hashtag TEXT NOT NULL,
            used INT
        )
    
    ''' %("hashTags",))
    print("created Hashtag table")
 
    con.commit()
 
createAccountsDatabase()
createHashtagDatabase()
