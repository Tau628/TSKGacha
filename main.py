from flask import Flask, render_template, request, flash, redirect, url_for
from replit import db, database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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
#Recursively sets ObservedLists and ObservedDicts to primitive lists and dicts.
#The Repl database uses these datatypes, so it's useful to convert when we need to do stuff.
def recurse_prim(x):
  x = database.to_primitive(x)
  if isinstance(x, dict):
    return {k:recurse_prim(v) for k,v in x.items()}
  if isinstance(x,list):
    return [recurse_prim(y) for y in x]
  return x



login_manager = LoginManager()
login_manager.init_app(web_site)

class User(UserMixin):
  def __init__(self, username):
    self.id = username

@login_manager.user_loader
def load_user(user_id):
  if user_id in db['players']:
    return User(user_id)
  else:
    return None




@web_site.route('/')
def home():
  if current_user.is_authenticated:
    return redirect(url_for('player_page', ply_ind = current_user.id))
  else:
    return render_template('home.html', user = current_user)


@web_site.route('/database')
def database_view():
  database = {k:recurse_prim(v) for k,v in db.items()}
  return render_template('database_view.html', user = current_user, database = database)

@web_site.route('/signup', methods=['GET','POST'])
def sign_up():
  if request.method == 'POST':
    #Gets all the information from the form
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
  
    #Checks the information to ensure that it is valid
    if username in db['players']:
        flash('Username already in use.', category='error')
    elif len(username) < 2:
        flash('First name must be greater than 1 character.', category='error')
    elif password1 != password2:
        flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
        flash('Password must be at least 7 characters.', category='error')
    else:
        #If none of these checks trigger, the information is valid
        #We now create a new user
        new_user = {
          'coins': 0,
          'max_roster': 3,
          'password': generate_password_hash(password1, method='sha256'),
          }
        
        #Adds user to database
        db['players'][username] = new_user

        #Automatically logs in the user
        login_user(User(username), remember=True)

        flash('Account created!', category='success')
        return redirect(url_for('home'))

  return render_template('sign_up.html', user = current_user)

@web_site.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    #Gets all the information from the form
    username = request.form.get('username')
    password = request.form.get('password')

    #Checks if the email exists in the database
    if username in db['players']:
      user = db['players'][username]

      #Checks if the password is valid
      if check_password_hash(user['password'], password):
        flash('Logged in successfully!', category='success')
        login_user(User(username), remember=True)
        return redirect(url_for('home'))
      else:
        flash('Incorrect password, try again.', category='error')
    else:
        flash('username does not exist.', category='error')
          
  return render_template('login.html', user = current_user)

@web_site.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@web_site.route('/characters/<chr_ind>')
def character_page(chr_ind):
  if current_user.is_authenticated:
    return render_template('character_page.html', user = current_user, character = database.to_primitive(db['characters'][int(chr_ind)]))
  else:
    return redirect(url_for('home'))

@web_site.route('/characters')
def characters():
  if current_user.is_authenticated:
    char_names = enumerate([c['name'] for c in db['characters']])
    return render_template('characters.html', user = current_user, char_names = char_names)
  else:
    return redirect(url_for('home'))

@web_site.route('/players/<ply_ind>')
def player_page(ply_ind):
  if current_user.is_authenticated:
    return render_template('player_page.html', user = current_user, player = (ply_ind, database.to_primitive(db['players'][ply_ind])))
  else:
    return redirect(url_for('home'))

@web_site.route('/players')
def players():
  if current_user.is_authenticated:
    player_names = db['players'].keys()
    return render_template('players.html', user = current_user, player_names = player_names)
  else:
    return redirect(url_for('home'))

if __name__ == '__main__':
  web_site.secret_key = 'super secret key'
  web_site.config['SESSION_TYPE'] = 'filesystem'

  web_site.run(host='0.0.0.0', port=8080, debug=True)