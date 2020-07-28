from igramscraper.instagram import Instagram
from config import USERNAME, PASSWORD, MAINPASSWORD, MAINUSERNAME
import requests
import sqlite3
from databaseConfig import DatabaseFunctions
import os



class InstaFunctions(Instagram):
    def __init__(self):
        Instagram.__init__(self)
        self.databaseFunc = DatabaseFunctions()
    def checkDBifNewUser(self): #Vor jedem neuen durchlauf wird diese funktion aufgerufen um zu schauen ob alles klar geht
        withoutID = self.databaseFunc.withoutID()
        if len(withoutID)!= 0:
            print(withoutID)
            for pairs in withoutID:
                username = pairs[0]
                print(username)
                user = self.get_account(username=username)
                identifier = user.identifier
                self.databaseFunc.writeInstaIDIntoDB(identifier,username)

    def downloadProfilePicture(self,url, name, dbID, type):
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
        i=0
        while i<1:
            self.checkDBifNewUser()
            listofUsersQuery = self.databaseFunc.getAllUserIDs()
            for pair in listofUsersQuery:
                try:
                    stories = self.get_stories(pair[0])
                    for story in stories:
                        username = story.owner  # User ID von instagram
                        instaID = story.owner.identifier
                        for oneStory in story.stories:
                            unixtime = oneStory.created_time  # gives back unixtime
                            storyID = oneStory.identifier
                            if oneStory.type == "image":
                                image_high_resolution_url = oneStory.image_high_resolution_url
                                Image_low_res_URL = oneStory.image_low_resolution_url
                                Image_Standard_Res_URL = oneStory.image_low_resolution_url
                                try:
                                    url = oneStory.image_high_resolution_url  # soll video url speichern wenn story ein video ist.
                                    self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                    continue
                                except AttributeError:
                                    print("No high resolution url")
                                try:
                                    url = oneStory.image_standard_resolution_url  # soll video url speichern wenn story ein video ist.
                                    self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                    continue
                                except AttributeError:
                                    print("No standard resolution url")
                                try:
                                    url = oneStory.image_low_resolution_url  # soll video url speichern wenn story ein video ist.
                                    self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                    continue
                                except AttributeError:
                                    print("No low resolution url")

                            elif oneStory.type == "video":
                                try:
                                    url = oneStory.video_standard_resolution_url  # soll video url speichern wenn story ein video ist.
                                    self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                    continue
                                except AttributeError:
                                    print("No standard resolution url")
                                try:
                                    url = oneStory.video_low_resolution_url  # soll video url speichern wenn story ein video ist.
                                    self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                    continue
                                except AttributeError:
                                    print("No Low Res URL Video")
                                try:
                                    url = oneStory.video_low_bandwith_url  # soll video url speichern wenn story ein video ist.
                                    self.downloadProfilePicture(url, storyID, pair[1], oneStory.type)
                                    continue
                                except AttributeError:
                                    print("No low bandwith url")
                except Exception as ex:
                    print(ex)
            i+=1



instagram = InstaFunctions()
instagram.with_credentials(MAINUSERNAME, MAINPASSWORD)
instagram.login(force=False, two_step_verificator=True)
instagram.ewigerLoop()