from flask import Flask
from replit import db

from blueprints.players import playersBP
from blueprints.characters import charactersBP
from blueprints.auth import authBP, login_manager
from blueprints.pull import pullBP
from blueprints.other import otherBP
from blueprints.trades import tradesBP

#db['trades'] = []
#Aspect radio for art: 1080:1920

func = lambda x: 1

#test
banners = {
  'base' : {
    'image' : 'https://gamepress.gg/feheroes/sites/fireemblem/files/2021-04/LegendarySigurdBanner.PNG',
    'name' : 'Default',
    'rates' : {1: 30, 2: 25, 3: 22, 4: 16, 5: 7},
    'weights' : "lambda char: 1",
    'active' : True,
    'description' : "The basic banner with default rates."
  },
  'test_banner' : {
    'image' : 'https://gamepress.gg/feheroes/sites/fireemblem/files/2021-05/Forces%20of%20Will.PNG',
    'name' : 'The Last Airbender',
    'rates' : None,
    'weights' : "lambda char: 1000 if char['series']=='Avatar: The Last Airbender' else 1",
    'active' : True,
    'description' : "Rate up for all Avatar: The Last Airbender characters."
  }
}
db['banners'] = banners



app = Flask(__name__)
login_manager.init_app(app)
app.register_blueprint(playersBP)
app.register_blueprint(charactersBP)
app.register_blueprint(authBP)
app.register_blueprint(pullBP)
app.register_blueprint(otherBP)
app.register_blueprint(tradesBP)

#Loads in database from JSON
'''
import json
for k in db.keys():
  del db[k]
with open('./sampledatabase.json') as f:
  data = json.load(f)
for k, v in data.items():
  db[k] = v
'''

if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(host='0.0.0.0', port=8080, debug=True)