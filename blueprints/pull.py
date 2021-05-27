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

def pickChar(banner_name=None):

  if banner_name is None:
    banner = db['banners']['base']
  else:
    banner = db['banners'][banner_name]

  #Gets a list of all owned characters
  owned_chars = getListOwnedChars()
  
  #Gets a list of characters filtering out the characters already owned
  viable_characters = {k:v for k,v in db['characters'].items() if k not in owned_chars}
  if viable_characters == {}:
    print('There are no characters at all')
    return None

  #Finds out if any rarities have no characters
  rarities = banner['rates']
  if rarities is None:
    rarities = db['banners']['base']['rates']

  valid_rarities = {
    r : 
    len(list(filter(
      lambda x: x['rarity']==int(r),
      viable_characters.values()
    )))>0
    for r in rarities.keys()
  }

  #Selects a rarity
  r_weights = [(r, w if valid_rarities[r] else 0) for r, w in rarities.items()]
  sum_weights = sum(map(lambda x: x[1], r_weights))
  r_weights  = [(r,float(w)/sum_weights) for r,w in r_weights]
  rarity_picked = int(np.random.choice(list(map(lambda x: x[0], r_weights)), p=list(map(lambda x: x[1], r_weights))))

  #Filters for selected rarity
  viable_characters = {k:v for k,v in viable_characters.items() if v['rarity']==rarity_picked}
  if viable_characters == {}:
    print('There are no characters within this rarity')
    return None
  
  #Picks character based on weighting function
  weight_function = eval(banner['weights'])
  print(weight_function)
  c_weights = [weight_function(c) for cid,c in viable_characters.items()]
  c_weights = [w/sum(c_weights) for w in c_weights]

  return np.random.choice(list(viable_characters.keys()), p=c_weights)


@pullBP.route('/pull', methods=['GET','POST'])
def pull():
  
  if request.method == 'POST':
    player = db['players'][current_user.id]
    button = request.form.get('submit_button')

    if button.split('-')[0] == 'pull':
      banner_name = button.split('-')[1]

      if player['coins'] <= 0:
        flash("You don't have enough coins.", category='error')

      else:

        #You don't a full roster
        if player['max_roster'] > len(player['roster']):
          new_char = pickChar(banner_name)
          db['players'][current_user.id]['roster'].append(new_char)

        #You do have a full roster
        else:
          new_char = pickChar(banner_name)
          db['players'][current_user.id]['pulled_character'] = new_char

        db['players'][current_user.id]['coins'] -= 1

    elif button == 'remove':
      removing = request.form.get('characterRemoving')
      if removing is not None:
        removing = removing.split('-')[1]
        if removing == 'pulled':
          db['players'][current_user.id]['pulled_character'] = None
        else:
          removing = int(removing)
          db['players'][current_user.id]['roster'].pop(removing)
          db['players'][current_user.id]['roster'].append(player['pulled_character'])
          db['players'][current_user.id]['pulled_character'] = None



  player = db['players'][current_user.id]
  can_pull = player['pulled_character'] is None

  char_ids = database.to_primitive(player['roster']) 
  characters = [(str(ri), db['characters'][ci]) for ri,ci in enumerate(char_ids)]
  if not can_pull:
    pulled_char = (player['pulled_character'], db['characters'][player['pulled_character']])
  else:
    pulled_char = None

  coins=player['coins']

  return render_template('pull/pull.html', user = current_user, can_pull = can_pull, coins=coins, coinstr = f"Pull: {coins}->{coins-1}", characters=characters, pulled_char = pulled_char, banners = db['banners'])