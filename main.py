from flask import Flask, render_template, request 
from replit import db, database
import pprint
import json
from random import choice

web_site = Flask(__name__)

for k in db.keys():
  del db[k]
with open('./sampledatabase.json') as f:
  data = json.load(f)
for k, v in data.items():
  db[k] = v

def recurse_prim(x):
  x = database.to_primitive(x)
  if isinstance(x, dict):
    return {k:recurse_prim(v) for k,v in x.items()}
  if isinstance(x,list):
    return [recurse_prim(y) for y in x]
  return x

data = {k:recurse_prim(v) for k,v in db.items()}


number_list = [
	100, 101, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 400, 401, 402, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415,
	416, 417, 418, 421, 422, 423, 424, 425, 426,
	429, 431, 444, 450, 451, 500, 502, 503, 504, 506, 507, 508, 509, 510, 511, 599
]

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

@web_site.route('/page')
def random_page():
  return render_template('page.html', code=choice(number_list))

@web_site.route('/database')
def database_view():
  return render_template('database_view.html', database = data, color=choice(['red','blue','green']))

web_site.run(host='0.0.0.0', port=8080, debug=True)