import os
import twint
import nest_asyncio
import sqlite3
import threading
from data_handling import Router
import json
import io
import time
 
class webScraper(Router):
    def __init__(self, dataBaseName, tableName1, tableName2, connection):
        super().__init__(dataBaseName, tableName1, tableName2, connection)
        self.dataBaseName = dataBaseName
        self.tableName1 = tableName1
        self.tableName2 = tableName2
        self.connection = connection
        self.maxValue = 60
        self.running = True

        self.totalPotentialIterations = 100000
        self.read = False
        self.bufferFile = "output.txt"
        self.currentHashtag = [1, 'Sales', True] #genesis
        self.waitTime = 0
        self.previousWaitTime = 0

        nest_asyncio.apply()
    
    def extractWords(self, file, character):
        results = []
        with io.open(file, mode = "r", encoding="utf8") as f:
            data = f.readlines()
            for datum in data:
                try:
                    jsonData = json.loads(datum)
                    for word in jsonData['tweet'].split():
                        if word[0] == character:
                            basic = word.replace(character, '') # removes the pound sign from the hashtag
                            results.append(basic)
                except:
                    print("error reading json")
        return results

    def extractUsers(self, file):
        users = []
        with io.open(file, mode = 'r', encoding='utf8') as f:
            data = f.readlines()
            for datum in data:
                try:
                    jsonData = json.loads(datum)
                    users.append(jsonData['username'])
                except:
                    print("error extracting user from file")
        return users

    def readPersistentData(self, file):
        with io.open(file, "r", encoding='utf8') as data:
            row = data.readlines()
            try:
                self.totalUsers = int(row[0].replace('Total Accounts: ', ''))
            except:
                self.totalUsers = 0
            try:
                self.totalHashtags = int(row[1].replace('Total Hashtags: ', ''))
            except:
                self.totalHashtags = 0
            try:
                self.totalIterations = int(row[2].replace('Total Iterations: ', ''))
            except:
                self.totalIterations = 0
            try:
                self.readHashtags = int(row[3].replace('Read Hashtags: ', ''))
            except:
                self.readHashtags = 0
            try:
                self.readAccounts = int(row[4].replace('Read Accounts: ', ''))
            except:
                self.readAccounts = 0

            self.read = True
        
        
    def writePersistentData(self, file):
        if not self.read:
            self.readPersistentData
        data = open(file, "w")
        data.close()
        data.write('''Total Accounts: %s\nTotal Hashtags: %s\n Total Iterations: %s\nRead Hashtags: %s\n Read Accounts: %s''' %(self.totalUsers, self.totalHashtags, self.totalIterations, self.readHashtags, self.readAccounts))
        data.close()

    def findHashtagsFromHashtag(self, hashtag):
        self.performSearch(hashtag, self.maxValue)
        p = self.extractWords(self.bufferFile, "#")
        return p

    def findHashtagsFromFile(self, file):
        p = self.extractWords(file, "#")
        return p
 
    def findHashtagFromUser(self, user):
        pass

    def findUsersFromHashtag(self, hashtag):
        self.performSearch(hashtag)
        users1 = self.extractUsers(self.bufferFile)
        users2 = self.extractWords(self.bufferFile, '@')
        return users1 + users2

    def performSearch(self, value, quantity):
        search = twint.Config()
        search.Search = value
        search.Limit = quantity
        search.Store_json = True
        search.Output = self.bufferFile

        self.clearFile(self.bufferFile)
        try:
            twint.run.Search(search)  
        except:
            print("There was a temporary IP ban, waiting 15 minutes")
            time.sleep(905)
            self.performSearch(value, self.maxValue)
        if self.waitTime != 0:
            self.waitTime = self.previousWaitTime
            self.previousWaitTime = 0
        print(self.waitTime)

    def start(self):
        self.readPersistentData()
        self.running = True
        self.searchLoop()
 
    def stop(self):
        self.running = False
        self.writePersistentData()
        super().finish()

    def readJsonFile(self, fileName):
        with open(fileName, encoding='utf8') as f:
            data = json.load(f)

        return data

    def getTweetsFromFile(self, fileName):
        info = []
        with io.open(fileName, encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                info.append(json.loads(line)['tweet'])
        return info

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
        except:
            print("error searching for" + str(person))
        try:
            data = self.readJsonFile(self.bufferFile)
            self.addAccountToDatabase(data['id'], data['username'], data['name'], data['tweets'], data['followers'], data['following'], data['location'], data['likes'], data['verified'], "I; // afdslk")
            print("account successfully added")
        except:
            print("Couldn't find account from username: " + username)

    def searchLoop(self):
        if not self.read:
            self.readPersistentData('Log_File.txt')
        #self.writePersistentData('Log_File.txt')

        while (self.totalIterations < self.totalPotentialIterations) and self.running:
            self.setValueRead(self.tableName2, self.currentHashtag[0], 'id')
            people = self.findUsersFromHashtag(self.currentHashtag[1])
            hashtags = self.findHashtagsFromHashtag(self.currentHashtag[1])
            self.readHashtags +=1
            print("completed search") 

            
            for person in people:
                self.addAccount(person)
                #hashtags += self.findHashtagFromUser(person)
                self.totalUsers +=1
            
            for hashtag in hashtags:
                self.addHashtagToDatabase(hashtag)
                self.totalHashtags +=1
            
            self.currentHashtag = self.getHashtag()
            self.totalIterations +=1
        self.stop()


#n = sqlite3.connect("Accounts.db")
#w = webScrapper("Accounts.db", "Accounts", "Hashtags", n)

#names = ["rihanna", "BillyM2k", "telsaownersSV", "BonJovi", "potus", "harvard", "ford", "tesla"]

#w.start()

#w.clearFile(w.bufferFile)
#twint.run.Search(c)

#w.searchLoop()
#w.extractHashtags("output.json")

#use gensim or word2vec for word similarity