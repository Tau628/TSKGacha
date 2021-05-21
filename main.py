from flask import Flask, render_template, request, flash, redirect, url_for
from replit import db, database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from blueprints.players import playersBP
from blueprints.characters import charactersBP
from blueprints.auth import authBP, login_manager
from blueprints.other import otherBP

#print(playersBP)

web_site = Flask(__name__)
login_manager.init_app(web_site)
web_site.register_blueprint(playersBP)
web_site.register_blueprint(charactersBP)
web_site.register_blueprint(authBP)
web_site.register_blueprint(otherBP)

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
  web_site.secret_key = 'super secret key'
  web_site.config['SESSION_TYPE'] = 'filesystem'

  web_site.run(host='0.0.0.0', port=8080, debug=True)