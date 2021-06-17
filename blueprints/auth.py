from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import time

authBP = Blueprint('authBP', __name__)

login_manager = LoginManager()

#Defines a simple class to keep track of users
class User(UserMixin):
  def __init__(self, username):
    self.id = username

#Loads user
@login_manager.user_loader
def load_user(user_id):
  if user_id in db['players']:
    return User(user_id)
  else:
    return None

#Sign up page
@authBP.route('/signup', methods=['GET','POST'])
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
          'roster': [],
          'pulled_character': None,
          'last_check_in': int(time.time()),
          'NSFW_shown': False,
          'wishlist' : [],
          }
        
        #Adds user to database
        db['players'][username] = new_user

        #Automatically logs in the user
        login_user(User(username), remember=False)

        flash('Account created!', category='success')
        return redirect(url_for('otherBP.home'))

  return render_template('authentication/sign_up.html', user = current_user)

#Log in page
@authBP.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    #Gets all the information from the form
    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('rememberMe')=='on'

    #Checks if the email exists in the database
    if username in db['players']:
      user = db['players'][username]

      #Checks if the password is valid
      if check_password_hash(user['password'], password):
        flash('Logged in successfully!', category='success')
        login_user(User(username), remember=remember)
        return redirect(url_for('otherBP.home'))
      else:
        flash('Incorrect password, try again.', category='error')
    else:
        flash('Username does not exist.', category='error')
          
  return render_template('authentication/login.html', user = current_user)

#Log out page
@authBP.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authBP.login'))
