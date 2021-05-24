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
    print(pickChar())
  return render_template('pull/pull.html', user = current_user)