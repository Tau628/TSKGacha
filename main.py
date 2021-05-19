from flask import Flask, render_template, request 
from replit import db, database
import pprint
import json
from random import choice

web_site = Flask(__name__)

#Loads in database from JSON
'''
for k in db.keys():
  del db[k]
with open('./sampledatabase.json') as f:
  data = json.load(f)
for k, v in data.items():
  db[k] = v
'''

def recurse_prim(x):
  x = database.to_primitive(x)
  if isinstance(x, dict):
    return {k:recurse_prim(v) for k,v in x.items()}
  if isinstance(x,list):
    return [recurse_prim(y) for y in x]
  return x

data = {k:recurse_prim(v) for k,v in db.items()}


@web_site.route('/')
def index():
  return render_template('index.html')

@web_site.route('/user/', defaults={'username': None})
@web_site.route('/user/<username>')
def generate_user(username):
  if not username:
    username = request.args.get('username')

  if not username:
    username = 'user'
    #return 'Sorry error something, malformed request.'

  return render_template('personal_user.html', user=username)


@web_site.route('/database')
def database_view():
  return render_template('database_view.html', database = data)

@web_site.route('/base')
def base():
  return render_template('base.html')

web_site.run(host='0.0.0.0', port=8080, debug=True)