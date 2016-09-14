import configparser

config = configparser.ConfigParser()
config.read('api.cfg')

API_KEY = config['DEFAULT']['api_key']

print(API_KEY)