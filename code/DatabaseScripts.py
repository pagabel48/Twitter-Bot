import sqlite3
 
DatabaseName = "Accounts"
 
def connectToDataBase(name):
    conn = sqlite3.connect(name + ".db")
 
    return conn
 
def createAccountsDatabase():
    conn = connectToDataBase(DatabaseName)
    conn.execute('''
        CREATE TABLE Accounts
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
            used INT,
            code TEXT
        );''')
    print("created Accounts table")

def createHashtagDatabase():
    con = connectToDataBase(DatabaseName)
    con.execute('''
        CREATE TABLE Hashtags
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hashtag TEXT NOT NULL,
            used INT
        )
    
    ''')
    print("created Hashtag table")
 
    con.commit()
 
createAccountsDatabase()
createHashtagDatabase()
