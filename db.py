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

	def configuredb(self):
		cur = self.con.cursor()

		cur.execute("""SELECT table_name
						FROM information_schema.tables
						WHERE table_schema='public'
						AND table_type='BASE TABLE';""")
		tablas = ""
		for x in cur.fetchall():
			tablas += "".join(x)

		if "players" not in tablas:
			print "Creating players table"
			sql = """CREATE TABLE players (
							id serial PRIMARY KEY, 
							name varchar, 
							realm varchar,
							ilvl integer,
							class integer,
							race integer,
							gender integer,
							lvl integer,
							faction integer,
							image varchar
						);"""
			cur.execute(sql)

			self.con.commit()

		if "itemsequiped" not in tablas:
			print "Creating itemsEquiped table"
			sql = """CREATE TABLE itemsEquiped (
							id serial PRIMARY KEY,
							idPlayer integer,
							idItem integer,
							context varchar,
							bonusList varchar,
							name varchar,
							part varchar,
							ilvl integer
			);"""
			cur.execute(sql)

			self.con.commit()

		cur.close()

	def connect(self):
		#try:
		self.con = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.DB_NAME, self.USER, self.DB_IP, self.PASS))
		self.configuredb()
		print "Conexion establecida"	
		return self.con
		#except:
		#	print "Imposible conectar a la base de datos"


	def disconnect(self):
		self.con.close()

	def insertPlayer(self, player):
		print "Insertando: " + player["name"]
		cur = self.con.cursor()
		sql = "INSERT INTO players VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"
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
		pid = cur.fetchone()[0]
		self.insertItem(player["items"], pid)

		self.con.commit()
		cur.close()
	
	def insertItem(self, items, id):
		print "Insertando: " + str(items["averageItemLevel"]) + " de: " + str(id)
		del items["averageItemLevelEquipped"]
		del items["averageItemLevel"]
		for item in items:
			key = item
			item = items[key]
			bonus = ",".join(str(item["bonusLists"]))
			cur = self.con.cursor()
			sql = "INSERT INTO itemsEquiped VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"
			cur.execute(sql, (
				id,
				item["id"],
				item["context"],
				bonus,
				item["name"],
				key,
				item["itemLevel"])
			)
			iid = cur.fetchone()[0]
			self.con.commit()
			cur.close()

	def insertStats(self, stat, id):
		print "Insertando: " + str(stat["stat"]) + "de: " + str(id)
		cur = self.con.cursor()
		sql = "INSERT INTO itemStats VALUES (DEFAULT, %s, %s, %s);"
		cur.execute(sql, (
			id,
			stat["stat"],
			stat["amount"])
		)

		self.con.commit()
		cur.close()

	def insertArmor(self, stat, id):
		cur = self.con.cursor()
		sql = "INSERT INTO itemStats VALUES (DEFAULT, %s, %s, %s);"
		cur.execute(sql, (
			id,
			-1,
			stat)
		)

		self.con.commit()
		cur.close()

	def getPlayers(self):
		cur = self.con.cursor()
		sql = "SELECT name FROM players"
		cur.execute(sql)
		return cur.fetchall()

#db = DBConection()
#db.connect()
