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

    replace = 1

    if player['coins'] <= 0:
      flash("You don't have enough coins.", category='error')

    else:

      #You don't a full roster
      if player['max_roster'] > len(player['roster']):
        flash('Who are you going to get...?')
        new_char = pickChar()
        db['players'][current_user.id]['roster'].append(new_char)

      #You do have a full roster
      
      elif replace is not None and (0 <= replace < len(player['roster'])):
        old_char = db['players'][current_user.id]['roster'][replace]
        flash(f"You're trading away someone")
        new_char = pickChar()
        db['players'][current_user.id]['roster'][replace] = new_char

      else:
        flash('Please select a character to replace.')
        return

      #if successful:
      db['players'][current_user.id]['coins'] -= 1
      #await ctx.send(f"Congratulations {player['name']}! You pulled...\n{formatCharacter(new_char)}You have {db['players'][user]['coins']} Koins left.")
  return render_template('pull/pull.html', user = current_user)