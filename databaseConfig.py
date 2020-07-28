import _sqlite3

# Eine Tabelle mit nur Primary Key und User ID
# Das Skript geht dann durch die BasisDB durch und richtet sich nicht nach einer festen liste im code, so dass man das Programm nicht abbrechen muss.
# Im zweifel soll man einfach den username eintragen können und nicht die ID, die ID sucht dann ggf. das Programm selbst raus

# BasisDB = Primary Key, InstaUserID, Username
# DatenDB = Primarykey, MediaID bei Download (Doppelte downloads vermeiden), Uhrzeit in Unixtime, MediaType (Video oder Image), Dateinamen nach erfolgtem Download


# ToDo:
# Datenbank nach oberem vorbild erstellen 20 min
# Prozedur um nur Username einzutragen und dann die ID zu beziehen und nachzutragen in der DB. Ansonsten ID benutzen und nicht username 10 Min
# Download von Datein und speichern im Ordner mit der ID des Users in der DB mit Dateinamen der in der DB steht 10 Min
# Ggf. anlegen von Verzeichnissen für User  30 Min
# Loop schreiben für dauerhafte ausführung nach bestimmter Zeitspanne (while True except break) 5 Min

