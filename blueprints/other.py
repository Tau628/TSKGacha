from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db, database
from flask_login import current_user


#Recursively sets ObservedLists and ObservedDicts to primitive lists and dicts.
#The Repl database uses these datatypes, so it's useful to convert when we need to do stuff.
def recurse_prim(x):
  x = database.to_primitive(x)
  if isinstance(x, dict):
    return {k:recurse_prim(v) for k,v in x.items()}
  if isinstance(x,list):
    return [recurse_prim(y) for y in x]
  return x


otherBP = Blueprint('otherBP', __name__)


@otherBP.route('/')
def home():
  if current_user.is_authenticated:
    return redirect(url_for('playersBP.player_page', ply_ind = current_user.id))
  else:
    return render_template('home.html', user = current_user)


@otherBP.route('/database')
def database_view():
  database = {k:recurse_prim(v) for k,v in db.items()}
  return render_template('database_view.html', user = current_user, database = database)


@otherBP.route('/dashboard', methods=['GET','POST'])
def dashboard():
  if request.method == 'POST':

    button = request.form.get('submit_button')
    
    if button == 'Give Kremkoin':
      db['players'][current_user.id]['coins'] += 1
      flash(f"You now have {db['players'][current_user.id]['coins']} koins!", category='success')

    elif button == 'Do Something Else':
      print('Do something else')
    else:
      print('Post but no button')

  if current_user.is_authenticated:
    return render_template('dashboard.html', user = current_user)
  else:
    return redirect(url_for('home'))
