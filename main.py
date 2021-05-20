from flask import Flask, render_template, request, flash, redirect, url_for
from replit import db, database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

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
def home():
  return render_template('home.html')


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
  

    if email in db['players']:
        flash('Email already in use.', category='error')
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
          'password': generate_password_hash(password1, method='sha256'),
          }
        
        db['players'][email] = new_user

        #login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return redirect(url_for('home'))

  return render_template('sign_up.html')

@web_site.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    if email in db['players']:
      user = db['players'][email]

      if check_password_hash(user['password'], password):
        flash('Logged in successfully!', category='success')
        #login_user(user, remember=True)
        return redirect(url_for('home'))
      else:
        flash('Incorrect password, try again.', category='error')
    else:
        flash('Email does not exist.', category='error')
          
  return render_template('login.html')

if __name__ == '__main__':
  web_site.secret_key = 'super secret key'
  web_site.config['SESSION_TYPE'] = 'filesystem'

  web_site.run(host='0.0.0.0', port=8080, debug=True)