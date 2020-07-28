from igramscraper.instagram import Instagram
from config import USERNAME, PASSWORD, MAINPASSWORD, MAINUSERNAME
import requests
import sqlite3
from databaseConfig import DatabaseFunctions

'''instagram = Instagram()
instagram.with_credentials(MAINUSERNAME, MAINPASSWORD)
instagram.login(force=False,two_step_verificator=True)
ACCOUNTNAME = "sarah._.wi"
account = instagram.get_account(ACCOUNTNAME)


listOfUsers = [account.identifier]  #In die Liste werden die Leute bzw. die IDs der Leute geschrieben von denen man die Stories haben möchte.
#ListOfUsers wird jedes mal aufs neue populiert werden um dann immer neu checken zu können ob neue Stories vorhanden sind.



stories = instagram.get_stories(listOfUsers)
for story in stories:
    print(story.owner)  #User ID von instagram
    print(story.owner.identifier)
    for oneStory in story.stories:
        print("Created time")
        print(oneStory.created_time)        #gives back unixtime
        print("Story ID")
        print(oneStory.identifier)
        if oneStory.type == "image":
            print("Image URL")
            print("image_high_resolution_url")
            print(oneStory.image_high_resolution_url)
            print("Image low res URL")
            print(oneStory.image_low_resolution_url)
            print("Image Standard Res URL")
            print(oneStory.image_low_resolution_url)

        elif oneStory.type == "video":
            print("Video URL")
            try:
                print(oneStory.video_standard_resolution_url)   #soll video url speichern wenn story ein video ist.
            except AttributeError:
                print("No standard resolution url")
            try:
                print(oneStory.video_low_resolution_url)
            except AttributeError:
               print("No Low Res URL Video")

            try:
                print(oneStory.video_low_bandwith_url)
            except AttributeError:
                print("No low bandwith url")
'''

#for story in stories.stories:
#    print(story)


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




instagram = InstaFunctions()
instagram.with_credentials(MAINUSERNAME, MAINPASSWORD)
instagram.login(force=False, two_step_verificator=True)


instagram.checkDBifNewUser()