from igramscraper.instagram import Instagram
from config import USERNAME, PASSWORD, MAINPASSWORD, MAINUSERNAME
import requests
import sqlite3
from databaseConfig import DatabaseFunctions
import os
import time
import sys
from datetime import datetime



class InstaFunctions(Instagram):
    def __init__(self):
        Instagram.__init__(self)
        self.databaseFunc = DatabaseFunctions()
    def checkDBifNewUser(self): #Vor jedem neuen durchlauf wird diese funktion aufgerufen um zu schauen ob alles klar geht
        withoutID = self.databaseFunc.withoutID()
        if len(withoutID)!= 0:
            print("Adding IDs to DB")
            print(withoutID)
            for pairs in withoutID:
                username = pairs[0]
                print(username)
                user = self.get_account(username=username)
                identifier = user.identifier
                self.databaseFunc.writeInstaIDIntoDB(identifier,username)

    def downloadProfilePicture(self,url, name, dbID, type):
        print(dbID, type, url)
        if not os.path.exists(str(dbID)):
            os.makedirs(str(dbID))

        response = requests.get(url)
        if type == "image":
            with open(os.path.join(str(dbID), name + ".jpg"), 'wb') as temp_file:
                temp_file.write(response.content)
        else:
            with open(os.path.join(str(dbID), name + ".mp4"), 'wb') as temp_file:
                temp_file.write(response.content)


    def ewigerLoop(self):
        #while True:
        self.checkDBifNewUser()
        listofUsersQuery = self.databaseFunc.getAllUserIDs()
        for pair in listofUsersQuery:
            try:
                stories = self.get_stories(pair[0])
                for story in stories:
                    username = story.owner  # User ID von instagram
                    print(username)
                    instaID = story.owner.identifier
                    for oneStory in story.stories:
                        unixtime = oneStory.created_time  # gives back unixtime
                        storyID = oneStory.identifier
                        if self.databaseFunc.checkIfStoryIDInDB(storyID) == True:
                            if oneStory.type == "image":
                                try:
                                    url = oneStory.image_high_resolution_url  # soll video url speichern wenn story ein video ist.
                                    if url != None:
                                        self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                        self.databaseFunc.writeDataInDB(pair[1], storyID, unixtime, oneStory.type) #Media ID ist dann auch der Name der Datei
                                        continue

                                except AttributeError:
                                    print("No high resolution url")
                                try:
                                    url = oneStory.image_standard_resolution_url  # soll video url speichern wenn story ein video ist.
                                    if url != None:
                                        self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                        self.databaseFunc.writeDataInDB(pair[1], storyID, unixtime, oneStory.type)
                                        print("Continue")
                                        continue
                                except AttributeError:
                                    print("No standard resolution url")
                                try:
                                    url = oneStory.image_low_resolution_url  # soll video url speichern wenn story ein video ist.
                                    if url != None:
                                        self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                        self.databaseFunc.writeDataInDB(pair[1], storyID, unixtime, oneStory.type)
                                        print("Continue")
                                        continue
                                except AttributeError:
                                    print("No low resolution url")
                            elif oneStory.type == "video":
                                try:
                                    url = oneStory.video_standard_resolution_url  # soll video url speichern wenn story ein video ist.
                                    if url != None:
                                        self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                        self.databaseFunc.writeDataInDB(pair[1], storyID, unixtime, oneStory.type)
                                        print("Continue")
                                        continue
                                except AttributeError:
                                    print("No standard resolution url")
                                try:

                                    url = oneStory.video_low_resolution_url  # soll video url speichern wenn story ein video ist.
                                    if url != None:
                                        self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                        self.databaseFunc.writeDataInDB(pair[1], storyID, unixtime, oneStory.type)
                                        print("Continue")
                                        continue
                                except AttributeError:
                                    print("No Low Res URL Video")
                                try:
                                    url = oneStory.video_low_bandwith_url  # soll video url speichern wenn story ein video ist.
                                    if url != None:
                                        self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                        self.databaseFunc.writeDataInDB(pair[1], storyID, unixtime, oneStory.type)
                                        print("Continue")
                                        continue
                                except AttributeError:
                                    print("No low bandwith url")
                        else:
                            print("Something strange is happenning.")
            except Exception as ex:
                print(ex)
                sys.exit(1)
            #now = datetime.now()
            #current_time = now.strftime("%H:%M:%S")
            #print("Paused since: ", current_time)
            #time.sleep(60 * 60)  # Eine Stunde warten bis die nächste anfrage kommt






instagram = InstaFunctions()
#instagram.with_credentials(MAINUSERNAME, MAINPASSWORD)
instagram.with_credentials(MAINUSERNAME, MAINPASSWORD)
instagram.login(force=False, two_step_verificator=True)
instagram.ewigerLoop()