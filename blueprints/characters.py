from flask import Blueprint, render_template, redirect, url_for, request
from replit import db, database
from flask_login import current_user

charactersBP = Blueprint('charactersBP', __name__, url_prefix='/characters')

@charactersBP.route('/<chr_ind>')
def character_page(chr_ind):
  if current_user.is_authenticated:
    return render_template('characters/character_page.html', user = current_user, character = database.to_primitive(db['characters'][chr_ind]), chr_ind = chr_ind)
  else:
    return redirect(url_for('home'))

@charactersBP.route('/')
def characters():
  if current_user.is_authenticated:
    char_list = [(url_for('charactersBP.character_page', chr_ind = i), i, char['name']) for i,char in db['characters'].items()]
    return render_template('characters/characters.html', user = current_user, char_list = char_list)
  else:
    return redirect(url_for('home'))

@charactersBP.route('/proposal', methods=['GET','POST'])
def proposal():
  if request.method == 'POST':
    #Gets all the information from the form
    print(request.form)
  return render_template('characters/proposal.html', user = current_user)