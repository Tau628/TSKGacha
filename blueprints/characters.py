from flask import Blueprint, render_template, redirect, url_for
from replit import db, database
from flask_login import current_user

charactersBP = Blueprint('charactersBP', __name__, url_prefix='/characters')

@charactersBP.route('/<chr_ind>')
def character_page(chr_ind):
  if current_user.is_authenticated:
    return render_template('characters/character_page.html', user = current_user, character = database.to_primitive(db['characters'][int(chr_ind)]))
  else:
    return redirect(url_for('home'))

@charactersBP.route('/')
def characters():
  if current_user.is_authenticated:
    char_names = [c['name'] for c in db['characters']]
    char_list = [(url_for('charactersBP.character_page', chr_ind = i), i, name) for i,name in enumerate(char_names)]
    return render_template('characters/characters.html', user = current_user, char_list = char_list)
  else:
    return redirect(url_for('home'))

#