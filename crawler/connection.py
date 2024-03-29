import configparser
import requests
import db

class Connection(object):


	def __init__(self):
		config = configparser.ConfigParser()
		config.read('api.cfg')

		self.API_KEY = config['DEFAULT']['api_key']
		self.LOCALE = config['DEFAULT']['locale']
		self.WOW = "wow"
		self.REGION = config['DEFAULT']['region']

	def requestJson(self, url):
		r = requests.get(url)
		while r.status_code != 200:
			r = requests.get(url)
		return r.json()

	# c.getGuildProfile(name="Resort", realm="C'thun", fields=["members", "achievements"])
	def getGuildProfile(self, name, realm, fields=None):
		name = name.lower().replace (" ", "%2C")
		realm = realm.lower().replace (" ", "%2C")
		if fields:
			fields = "%2C".join(fields)

		url = "https://%s.api.battle.net/%s/guild/%s/%s?fields=%s&locale=%s&apikey=%s" % (self.REGION, self.WOW, realm, name, fields, self.LOCALE, self.API_KEY)
		return self.requestJson(url)

	# c.getMemberProfile(name="Raksus", realm="C'thun", fields=["items"])
	def getMemberProfile(self, name, realm, fields=None):
		name = name.lower().replace (" ", "%2C")
		realm = realm.lower().replace (" ", "%2C")
		if fields:
			fields = "%2C".join(fields)

		url = "https://%s.api.battle.net/%s/character/%s/%s?fields=%s&locale=%s&apikey=%s" % (self.REGION, self.WOW, realm, name, fields, self.LOCALE, self.API_KEY)
		return self.requestJson(url)