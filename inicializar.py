import connection
import db

c = connection.Conection()
data = dbDBConection()
data.connect()

for player in c.getGuildProfile(name="Resort", realm="C'thun", fields=["members"])["members"]:
	if player["character"]["level"] == 110 and player["rank"] not in (6, 7):
		json = c.getMemberProfile(name=player["character"]["name"], realm="C'thun", fields=["items"])
		data.insertPlayer(json)

data.disconnect()
