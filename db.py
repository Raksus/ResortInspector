import configparser
import psycopg2

class DBConection(object):

	def __init__(self):
		config = configparser.ConfigParser()
		config.read('db.cfg')

		self.DB_NAME = config['DEFAULT']['db_name']
		self.DB_IP = config['DEFAULT']['db_ip']
		self.USER = config['DEFAULT']['user']
		self.PASS = config['DEFAULT']['pass']

	def configuredb(self, con):
		cur = con.cursor()

		cur.execute("""SELECT table_name
						FROM information_schema.tables
						WHERE table_schema='public'
						AND table_type='BASE TABLE';""")
		tablas = ""
		for x in cur.fetchall():
			tablas += "".join(x)

		if "players" not in tablas:
			print "Creating players table"
			cur.execute("CREATE TABLE players (id serial PRIMARY KEY, name varchar, lvl integer);")
			con.commit()

	def connect(self):
		try:
			con = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.DB_NAME, self.USER, self.DB_IP, self.PASS))
			self.configuredb(con)
			print "Conexion establecida"	
			return con
		except:
			print "Imposible conectar a la base de datos"

	def insertPlayer(player):
		return None

db = DBConection()
db.connect()