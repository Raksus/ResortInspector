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
		print "Insertando: " + player["name"]
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
		print "Insertando: " + str(items["averageItemLevel"]) + " de: " + str(id)
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
		part["finger2"] = 12
		part["trinket1"] = 13
		part["trinket2"] = 14
		part["mainHand"] = 15
		part["offHand"] = 16
		part["shirt"] = 17

		itemArray = []
		for item in items:
			key = item
			item = items[key]
			bonus = ",".join(str(b) for b in item["bonusLists"])
			cur = self.con.cursor()
			sql = """INSERT INTO inspector_item("idItem", name, context, "bonusList", "itemSocket") 
				SELECT %s, %s, %s, %s, %s
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
				item["id"],
				item["context"],
				bonus,
				part[key])
			)
			itemId = None
			try:
				itemId = cur.fetchone()[0]
				itemArray.append(itemId)
			except:
				print "Ya estaba"
			cur.close()
			self.con.commit()

			if itemId != None:
				self.insertStats(item, itemId)

		return itemArray

	def insertStats(self, item, id):
		print "Insertando: " + "cosas " + "de: " + str(id)
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
		cur = self.con.cursor()
		sql = """INSERT INTO inspector_playeritem VALUES (DEFAULT, %s, %s)"""
		cur.execute(sql, (
			itemId,
			playerId)
		)

	def getPlayers(self):
		cur = self.con.cursor()
		sql = "SELECT name FROM players"
		cur.execute(sql)
		return cur.fetchall()

	def backup(self):
		cur = self.con.cursor()
		copy = "INSERT INTO itemshistoric SELECT * FROM itemsequiped, now();"
		cur.execute(copy)
		truncate = "TRUNCATE TABLE itemsequiped;"
		cur.execute(truncate)

#db = DBConection()
#db.connect()
