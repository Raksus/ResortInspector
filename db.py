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

		if "actualItems" not in tablas:
			print "Creating actualItems table"
			sql = """CREATE TABLE actualItems (
							id serial PRIMARY KEY,
							idPlayer integer,
							idItem integer,
							name varchar,
							ilvl integer
			);"""
			cur.execute(sql)

			self.con.commit()

		if "itemStats" not in tablas:
			print "Creating itemStats table"
			sql = """CREATE TABLE itemStats (
							id serial PRIMARY KEY,
							idItem integer,
							stat integer,
							amount integer
			);"""
			cur.execute(sql)

			self.con.commit
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
		con.close()

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
		for item in items:
			print item
			if not isinstance(item, basestring):
				cur = self.con.cursor()
				print "Ha pasado"
				sql = "INSERT INTO actualItems VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING id;"
				cur.execute(sql, (
					id,
					item["id"],
					item["name"],
					item["itemLevel"])
				)
				iid = cur.fetchone()[0]
				self.con.commit()
				cur.close()

				for stat in item["stats"]:
					self.insertStats(stat, iid)
				if item.has_key("armor"):
					armor = json.dumps({"stat": -1, "amount": item["armor"]})
					self.insertStats(armor, iid)

	def insertStats(self, stat, id):
		print "Insertando: " + stat + "de: " + id
		sql = "INSERT INTO itemStats VALUES (DEFAULT, %s, %s, %s);"
		cur.execute(sql, (
			id,
			stat["stat"],
			stat["amount"])
		)

		self.con.commit()
		cur.close()

#db = DBConection()
#db.connect()