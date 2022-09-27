
from operator import truediv
import twint
import nest_asyncio
import sqlite3
import threading
from data_handling import Router
import subprocess
import pandas as pd
import json
 
class webScrapper(Router):
    def __init__(self, dataBaseName, tableName1, tableName2, connection):
        super().__init__(dataBaseName, tableName1, tableName2, connection)
        self.dataBaseName = dataBaseName
        self.tableName1 = tableName1
        self.tableName2 = tableName2
        self.connection = connection

        self.bufferFile = "output.json"

    def findUsersFromHashtag(self):
        self.interface.run.Search()
 
    def findHashtagFromUsers(self, user):
        if (self.running == False):
            return
        else:
            pass
 
    def start(self):
        self.running = True
 
    def stop(self):
        self.running = False
        super().finish()

    def readJsonFile(self, fileName):
        with open(fileName) as f:
            data = json.load(f)

        return data

    def clearFile(self, file):
        f = open(file, "w")
        f.close()

    def addAccount(self, username):
        self.clearFile(self.bufferFile)

        person = twint.Config()
        person.Username = username
        person.Store_json = True
        person.Output = self.bufferFile
        try:
            twint.run.Lookup(person)
            data = self.readJsonFile(self.bufferFile)
            super().addAccountToDatabase(data['id'], data['username'], data['name'], data['tweets'], data['followers'], data['following'], data['location'], data['likes'], data['verified'])
            self.clearFile(self.bufferFile)
            print("account successfully added")
        except:
            print("Couldn't find account from username: " + username)

    def loop(self):
        if(self.running == False):
            pass

n = sqlite3.connect("Accounts.db")
w = webScrapper("Accounts.db", "Accounts", "hashTags", n)

names = ["rihanna", "BillyM2k", "teslaownersSV", "bonjovi"]

for name in names:
    w.addAccount(name)