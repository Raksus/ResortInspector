import configparser
import psycopg2
import json

class DBConection(object):

	def __init__(self):
		config = configparser.ConfigParser()
		config.read('db.cfg')

		self.DB_NAME = config['DEFAULT']['db_name']
		self.DB_IP = config['DEFAULT']['db_ip']
		self.USER = config['DEFAULT']['user']
		self.PASS = config['DEFAULT']['pass']

		self.con = None

	def connect(self):
		try:
			self.con = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.DB_NAME, self.USER, self.DB_IP, self.PASS))
			print "Conexion establecida"	
			return self.con
		except:
			print "Imposible conectar a la base de datos"


	def disconnect(self):
		try:
			self.con.close()
			print "Desconexion realizada"
		except:
			print "Error al desconectar"

	def insertPlayer(self, player):
		print "Insertando: " + str(player["id"])
		cur = self.con.cursor()
		sql = "INSERT INTO inspector_player VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"
		cur.execute(sql, (
			player["name"], 
			player["realm"], 
			player["items"]["averageItemLevelEquipped"],
			player["class"], 
			player["race"], 
			player["gender"], 
			player["level"], 
			player["faction"], 
			player["thumbnail"])
		)

		playerId = cur.fetchone()[0]
		self.con.commit()
		cur.close()
		return playerId
	
	def insertItem(self, items):
		del items["averageItemLevelEquipped"]
		del items["averageItemLevel"]
		part = {}
		part["head"] = 0
		part["neck"] = 1
		part["shoulder"] = 2
		part["back"] = 3
		part["chest"] = 4
		part["tabard"] = 5
		part["wrist"] = 6
		part["hands"] = 7
		part["waist"] = 8
		part["legs"] = 9
		part["feet"] = 10
		part["finger1"] = 11
		part["finger2"] = 11
		part["trinket1"] = 12
		part["trinket2"] = 12
		part["mainHand"] = 13
		part["offHand"] = 14
		part["shirt"] = 15

		itemArray = []
		artifact = None
		for item in items:
			key = item
			item = items[key]
			bonus = ",".join(str(b) for b in item["bonusLists"])
			cur = self.con.cursor()
			sql = """INSERT INTO inspector_item("idItem", name, context, "bonusList", "itemSocket", ilvl) 
				SELECT %s, %s, %s, %s, %s, %s
				WHERE NOT EXISTS 
					(SELECT "idItem", context, "bonusList", "itemSocket"
					FROM inspector_item
					WHERE "idItem" = %s AND context = %s AND "bonusList" = %s AND "itemSocket" = %s) 
				RETURNING id;"""
			cur.execute(sql, (
				item["id"],
				item["name"],
				item["context"],
				bonus,
				part[key],
				item["itemLevel"],
				item["id"],
				item["context"],
				bonus,
				part[key])
			)

			self.con.commit()

			nuevo = False
			try:
				print cur.fetchone()[0]
				if cur.fetchone() != None:
					nuevo = True
			except:
				nuevo = False

			itemId = None
			sql = """SELECT id FROM inspector_item WHERE "idItem" = %s AND context = %s AND "bonusList" = %s AND "itemSocket" = %s """
			cur.execute(sql, (
				item["id"],
				item["context"],
				bonus,
				part[key])
			)			
			itemId = cur.fetchone()[0]
			itemArray.append([itemId, key])

			cur.close()
			self.con.commit()

			if item["artifactId"] != 0:
				artifact = item

			if nuevo:
				self.insertStats(item, itemId)
			else:
				print "Ya estaba"

		print itemArray
		return itemArray, artifact

	def insertStats(self, item, id):
		cur = self.con.cursor()
		for stat in item["stats"]:
			sql = "INSERT INTO inspector_itemstats VALUES (DEFAULT, %s, %s, %s);"
			cur.execute(sql, (
				stat["stat"],
				stat["amount"],
				id)
			)
		
		armor = "INSERT INTO inspector_itemstats VALUES (DEFAULT, %s, %s, %s);"
		cur.execute(armor, (
			-1,
			item["armor"],
			id)
		)

		self.con.commit()
		cur.close()

	def insertPlayerItem(self, playerId, itemId):
		print "Item: " + str(itemId[0]) + ", de jugador: " + str(playerId)
		part = {}
		part["head"] = 0
		part["neck"] = 1
		part["shoulder"] = 2
		part["back"] = 3
		part["chest"] = 4
		part["tabard"] = 5
		part["wrist"] = 6
		part["hands"] = 7
		part["waist"] = 8
		part["legs"] = 9
		part["feet"] = 10
		part["finger1"] = 11
		part["finger2"] = 12
		part["trinket1"] = 13
		part["trinket2"] = 14
		part["mainHand"] = 15
		part["offHand"] = 16
		part["shirt"] = 17

		cur = self.con.cursor()
		sql = """SELECT "idItem_id", id FROM inspector_playeritem WHERE "idPlayer_id" = %s AND "itemSocket" = %s;"""
		cur.execute(sql, (
			playerId,
			part[itemId[1]])
		)

		try:
			update = cur.fetchone()
			print update
			if update[0] != itemId[0]:
				updatesql = """UPDATE inspector_playeritem SET "idItem_id" = %s WHERE id = %s AND "itemSocket" = %s;"""
				cur.execute(updatesql, (
					itemId[0],
					update[1],
					part[itemId[1]])
				)
				self.insertPlayerItemHistoric(playerId, update[0], part[itemId[1]])

		except:
			insertsql = """INSERT INTO inspector_playeritem VALUES (DEFAULT, %s, %s, %s);"""
			cur.execute(insertsql, (
				itemId[0],
				playerId,
				part[itemId[1]])
			)
		finally:
			self.con.commit()

		cur.close()

	def insertPlayerItemHistoric(seld, player Id, itemId, socket):
		cur = self.con.cursor()
		sql = """INSERT INTO inspector_playeritemhistoric("idItem_id", "idPlayer_id", "itemSocket") VALUES (%s, %s, %s)"""
		cur.execute(sql, (
			itemId,
			playerId,
			socket)
	)

	def insertArtifact(self, artifact, playerId):
		cur = self.con.cursor()
		idArtifact = artifact["artifactId"]
		sql = """INSERT INTO inspector_artifact("idArtifact", name, "idPlayer_id") 
					SELECT %s, %s, %s
					WHERE NOT EXISTS
						(SELECT "idArtifact", name, "idPlayer_id"
						FROM inspector_artifact
						WHERE "idArtifact" = %s AND name = %s AND "idPlayer_id" = %s);"""
		cur.execute(sql, (
			idArtifact,
			artifact["name"],
			playerId,
			idArtifact,
			artifact["name"],
			playerId)
		)
		
		self.con.commit()

		sql = """SELECT id FROM inspector_artifact WHERE "idArtifact" = %s;"""
		cur.execute(sql, [idArtifact])

		self.con.commit()
		idArtifact = cur.fetchone()[0]

		for relic in artifact["relics"]:
			idRelic, socket = self.insertRelic(relic)
			self.insertArtifactRelic(idRelic, socket, playerId, idArtifact)

		for trait in artifact["artifactTraits"]:
			self.insertTrait(trait, idArtifact, playerId)

		cur.close()

	def insertRelic(self, relic):
		cur = self.con.cursor()
		bonus = ",".join(str(b) for b in relic["bonusLists"])
		sql = """INSERT INTO inspector_relic("idRelic", context, "bonusList")
					SELECT %s, %s, %s
					WHERE NOT EXISTS
						(SELECT"idRelic", context, "bonusList"
						FROM inspector_relic
						WHERE "idRelic" = %s AND context = %s AND "bonusList" = %s);"""
		cur.execute(sql, (
			relic["itemId"],
			relic["context"],
			bonus,
			relic["itemId"],
			relic["context"],
			bonus)
		)
		self.con.commit()

		cur.execute("""SELECT id FROM inspector_relic 
				WHERE "idRelic" = %s;""", [relic["itemId"]])
		id = cur.fetchone()[0]
		
		self.con.commit()
		cur.close()

		return id, relic["socket"]

	def insertArtifactRelic(self, idRelic, socket, playerId, idArtifact):
		cur = self.con.cursor()
		sql = """SELECT "idRelic_id", id FROM inspector_artifactrelic WHERE "idPlayer_id" = %s AND "socket" = %s AND "idArtifact_id" = %s;"""
		cur.execute(sql, (
			playerId,
			socket,
			idArtifact)
		)

		try:
			update = cur.fetchone()
			if update[0] != idRelic:
				updatesql = """UPDATE inspector_artifactrelic SET "idRelic_id" = %s WHERE id = %s;"""
				cur.execute(updatesql, (
					idRelic,
					update[1]))
				self.insertArtifactRelicHistoric(update[0], socket, playerId, idArtifact)

		except:
			insertsql = """INSERT INTO inspector_artifactrelic("idPlayer_id", "idArtifact_id", "idRelic_id", socket) VALUES (%s, %s, %s, %s);"""
			cur.execute(insertsql, (
				playerId,
				idArtifact,
				idRelic,
				socket)
			)
		finally:
			self.con.commit()

		cur.close()

	def insertArtifactRelicHistoric(self, idRelic, socket, playerId, idArtifact):
		cur = self.con.cursor()
		sql = """INSERT INTO inspector_artifactrelichistoric("idPlayer_id", "idArtifact_id", "idRelic_id", socket) VALUES (%s, %s, %s, %s);"""
		cur.execute(sql, (
			playerId,
			idArtifact,
			idRelic,
			socket)
		)

	def insertTrait(self, trait, idArtifact, playerId):
		cur = self.con.cursor()
		sql = """SELECT id FROM inspector_trait WHERE "idTrait" = %s AND "idArtifact_id" = %s AND "idPlayer_id" = %s;"""
		cur.execute(sql, (
			trait["id"],
			idArtifact,
			playerId)
		)

		try:
			update = cur.fetchone()[0]
			updatesql = """UPDATE inspector_trait SET rank = %s WHERE id = %s;"""
			cur.execute(updatesql, (
				trait["rank"],
				update))
		except:
			insertsql = """INSERT INTO inspector_trait("idTrait", rank, "idArtifact_id", "idPlayer_id") VALUES (%s, %s, %s, %s);"""
			cur.execute(insertsql, (
				trait["id"],
				trait["rank"],
				idArtifact,
				playerId)
			)
		finally:
			self.con.commit()

		cur.close()

	def getPlayers(self):
		cur = self.con.cursor()
		sql = "SELECT name FROM players;"
		cur.execute(sql)
		return cur.fetchall()

#db = DBConection()
#db.connect()
