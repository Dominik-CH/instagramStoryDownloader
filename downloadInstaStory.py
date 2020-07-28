from igramscraper.instagram import Instagram
from config import USERNAME, PASSWORD, MAINPASSWORD, MAINUSERNAME
import requests
import sqlite3


instagram = Instagram()
instagram.with_credentials(MAINUSERNAME, MAINPASSWORD)
instagram.login(force=False,two_step_verificator=True)
ACCOUNTNAME = "pewdiepie"
account = instagram.get_account(ACCOUNTNAME)


listOfUsers = [account.identifier]  #In die Liste werden die Leute bzw. die IDs der Leute geschrieben von denen man die Stories haben möchte.
#ListOfUsers wird jedes mal aufs neue populiert werden um dann immer neu checken zu können ob neue Stories vorhanden sind.



stories = instagram.get_stories(listOfUsers)
print(stories)
for story in stories:
    print(story.owner)
    print(story.owner.id)
    for oneStory in story.stories:
        print(oneStory)
        print("Created time")
        print(oneStory.created_time)        #gives back unixtime
        print("Video URL")
        print(oneStory.video_standard_resolution_url)   #soll video url speichern wenn story ein video ist.
        print(oneStory.video_low_resolution_url)
        print(oneStory.video_low_bandwith_url)

#for story in stories.stories:
#    print(story)