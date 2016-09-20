import connection
import db

c = connection.Connection()
data = db.DBConection()
data.connect()

for player in c.getGuildProfile(name="Resort", realm="C'thun", fields=["members"])["members"]:
	if player["character"]["level"] == 110 and player["rank"] not in (6, 7):
		json = c.getMemberProfile(name=player["character"]["name"], realm="C'thun", fields=["items"])
		playerId = data.insertPlayer(json)
		items = data.insertItem(json["items"])
		for item in items:
			insertPlayerItem(playerId, item)

data.disconnect()
