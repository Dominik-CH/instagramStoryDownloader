import sqlite3
from igramscraper import instagram
import time

# ToDo:

# Download von Datein und speichern im Ordner mit der ID des Users in der DB mit Dateinamen der in der DB steht 10 Min
# Ggf. anlegen von Verzeichnissen für User  30 Min
# Loop schreiben für dauerhafte ausführung nach bestimmter Zeitspanne (while True except break) 5 Min

class DatabaseFunctions:
    def __init__(self):
        self.dbName = "storydetails.db"
    def createDatabase(self):
        dbName = self.dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute('''CREATE TABLE baseTable
                     (dbID INTEGER PRIMARY KEY AUTOINCREMENT, instaID text, username text)''')
        c.execute('''CREATE TABLE storyInfo
                     (userID INTEGER, mediaID text, unixtime text, mediaType text, FOREIGN KEY(userID) REFERENCES baseTable(dbID))''')
        conn.commit()
        conn.close()
        return dbName
    def writeInstaIDIntoDB(self,instaID,username):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("""UPDATE baseTable SET instaID = ? WHERE username =? """,(instaID,username,))
        conn.commit()
        conn.close()
    def getAllUserIDs(self):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("""SELECT instaID,dbID FROM baseTable""")
        ids = c.fetchall()
        conn.close()
        return ids

    def withoutID(self):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("""SELECT username,dbID FROM baseTable WHERE instaID IS NULL""")
        withoutIDs = c.fetchall()
        conn.close()
        return withoutIDs

    def checkIfStoryIDInDB(self,storyID):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("""SELECT mediaType, userID FROM storyInfo WHERE mediaID =?""",(storyID,))
        withoutIDs = c.fetchone()
        conn.close()
        print(withoutIDs)
        if withoutIDs == None:
            print("Muss runtergeladen werden ")
            return True
        else:
            print("MUSS NICHT runtergeladen werden")
            return False

    def writeDataInDB(self, userID, mediaID, unixtime, mediaType):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("""insert into storyInfo (userID , mediaID , unixtime , mediaType) values (?,?,?,?)""",
                  (userID, mediaID, unixtime, mediaType,))
        conn.commit()
        conn.close()

    def fetchDBIDbyinstaID(self,instaID):
        conn = sqlite3.connect(self.dbName)
        c = conn.cursor()
        c.execute("""SELECT dbID FROM baseTable WHERE instaID=?""",(instaID,))
        dbID = c.fetchone()
        conn.close()
        return dbID[0]  #Damit gleich die ID übergeben wird und nicht das Tuple

#idk = DatabaseFunctions()
#idk.createDatabase()
#idk.writeDataInDB(1,"15","52","15")
