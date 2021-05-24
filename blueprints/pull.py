from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db, database
from flask_login import current_user
import numpy as np

pullBP = Blueprint('pullBP', __name__)

def getListOwnedChars():
  characters = []
  for p in db['players'].values():
    characters += p['roster']
  return characters

def pickChar():
  rarities = list(map(int, db['rates'].keys()))
  weights  = list(db['rates'].values())
  weights  = [float(w)/sum(weights) for w in weights]
  rarity_picked = np.random.choice(rarities, p=weights)

  owned_chars = getListOwnedChars()
  
  viable_characters = {k:v for k,v in db['characters'].items() if k not in owned_chars}
  if viable_characters == {}:
    print('There are no characters at all')
    return None
  
  viable_characters = {k:v for k,v in viable_characters.items() if v['rarity']==rarity_picked}
  if viable_characters == {}:
    print('There are no characters within this rarity')
    return None
  
  print(rarity_picked)
  choices = list(viable_characters.keys())
  return np.random.choice(choices)


@pullBP.route('/pull', methods=['GET','POST'])
def pull():
  
  if request.method == 'POST':
    player = db['players'][current_user.id]
    button = request.form.get('submit_button')

    if button == 'pull':

      if player['coins'] <= 0:
        flash("You don't have enough coins.", category='error')

      else:

        #You don't a full roster
        if player['max_roster'] > len(player['roster']):
          new_char = pickChar()
          db['players'][current_user.id]['roster'].append(new_char)

        #You do have a full roster
        else:
          new_char = pickChar()
          db['players'][current_user.id]['pulled_character'] = new_char

        db['players'][current_user.id]['coins'] -= 1

    elif button == 'remove':
      db['players'][current_user.id]['pulled_character'] = None

  player = db['players'][current_user.id]
  can_pull = player['pulled_character'] is None

  char_ids = database.to_primitive(player['roster']) 
  characters = [(str(ri), db['characters'][ci]) for ri,ci in enumerate(char_ids)]
  if not can_pull:
    pulled_char = (player['pulled_character'], db['characters'][player['pulled_character']])
  else:
    pulled_char = None

  return render_template('pull/pull.html', user = current_user, can_pull = can_pull, characters=characters, pulled_char = pulled_char)