from flask import Flask, render_template, request, flash
from replit import db, database

web_site = Flask(__name__)

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

def recurse_prim(x):
  x = database.to_primitive(x)
  if isinstance(x, dict):
    return {k:recurse_prim(v) for k,v in x.items()}
  if isinstance(x,list):
    return [recurse_prim(y) for y in x]
  return x




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
  database = {k:recurse_prim(v) for k,v in db.items()}
  return render_template('database_view.html', database = database)

@web_site.route('/base')
def base():
  return render_template('base.html')

@web_site.route('/signup', methods=['GET','POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email')
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
  

    if False: ###IF USER EXISTS
        flash('Email already exists.', category='error')
    elif len(email) < 4:
        flash('Email must be greater than 3 characters.', category='error')
    elif len(username) < 2:
        flash('First name must be greater than 1 character.', category='error')
    elif password1 != password2:
        flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
        flash('Password must be at least 7 characters.', category='error')
    else:
        new_user = {
          'coins': 0,
          'max_roster': 3,
          'username': username,
          'password': password1,
          }
        
        db['players'][email] = new_user

        #login_user(new_user, remember=True)
        flash('Account created!', category='success')
        #return redirect(url_for('views.home'))

  return render_template('sign_up.html')

@web_site.route('/login', methods=['GET','POST'])
def login():
  return render_template('login.html')

if __name__ == '__main__':
  web_site.secret_key = 'super secret key'
  web_site.config['SESSION_TYPE'] = 'filesystem'

  web_site.run(host='0.0.0.0', port=8080, debug=True)