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


			);"""
			cur.execute(sql)

			self.con.commit()

	def connect(self):
		try:
			self.con = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.DB_NAME, self.USER, self.DB_IP, self.PASS))
			self.configuredb()
			print "Conexion establecida"	
			return self.con
		except:
			print "Imposible conectar a la base de datos"

	def insertPlayer(self, player):
		print "Insertando: " + player["name"]
		cur = self.con.cursor()
		sql = "INSERT INTO players VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"
		cur.execute(sql, 
			(player["name"], 
			player["realm"], 
			player["class"], 
			player["race"], 
			player["gender"], 
			player["level"], 
			player["faction"], 
			player["thumbnail"]))
		print cur.fetchone()[0]
		
		self.con.commit()
		

#db = DBConection()
#db.connect()