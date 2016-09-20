import connection
import db

c = connection.Connection()

c.getGuildProfile(name="Resort", realm="C'thun", fields=["members"])

c.getMemberProfile(name="Raksus", realm="C'thun", fields=["items"])

data = db.DBConection()

data.connect()

data.disconnect()
