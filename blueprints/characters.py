from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db, database
from flask_login import current_user

charactersBP = Blueprint('charactersBP', __name__, url_prefix='/characters')

from .pull import getOwnedChars,getPulledChars

@charactersBP.route('/<chr_ind>', methods=['GET','POST'])
def character_page(chr_ind):

  if request.method == 'POST':
    #button = request.form.get('submit_button')
    
    if chr_ind in db['players'][current_user.id]['wishlist']:
      db['players'][current_user.id]['wishlist'].remove(chr_ind)
      flash('Removed character from wishlist.', category='success')
    else:
      db['players'][current_user.id]['wishlist'].append(chr_ind)
      flash('Added character to wishlist.', category='success')
  
  #Determines if a characer is owned
  owned = getOwnedChars()
  if chr_ind in owned:
    owner = owned[chr_ind]
  else:
    owner = None
  pulled = getPulledChars()
  if chr_ind in pulled:
    puller = pulled[chr_ind]
  else:
    puller = None

  character = database.to_primitive(db['characters'][chr_ind])
  rarity = db['rarity_names'][str(character['rarity'])]
  rarity += " " + "☆"*character['rarity']
  
  in_wishlist = chr_ind in db['players'][current_user.id]['wishlist']
  players_wished = [pname for pname,player in db['players'].items() if chr_ind in player['wishlist']]

  return render_template('characters/character_page.html', user = current_user, character = character, chr_ind = chr_ind, owner=owner, puller=puller, rarity = rarity, in_wishlist=in_wishlist, players_wished=players_wished)

@charactersBP.route('/')
def characters():
  if current_user.is_authenticated:
    char_list = [(url_for('charactersBP.character_page', chr_ind = i), i, char) for i,char in sorted(db['characters'].items(), key=lambda x:int(x[0]))]
    
    return render_template('characters/characters.html', user = current_user, char_list = char_list)
  else:
    return redirect(url_for('otherBP.home'))

@charactersBP.route('/proposal', methods=['GET','POST'])
def proposal():
  if request.method == 'POST':
    button = request.form.get('submit_button')

    if button == 'propose':
      #Gets all the information from the form
      name = request.form.get('char_name')
      series = request.form.get('char_series')

      print(f'name:   {len(name)}')
      print(f'series: {len(series)}')
    
      #Checks the information to ensure that it is valid
      if  len(name) == 0 or len(series) == 0 :
          flash('Please type a name and a series.', category='error')
      else:
      
        new_char = {
          'image': None,
          'name': name,
          'status': 'pending',
          'series': series,
          'suggested_by': None,
          'suggested_timestamp': 'now, duh',
          'approval_votes': {},
          'rarity_votes': {}
        }

        db['proposed_characters'].append(new_char)
        flash('Character proposed!', category='success')
    
    elif button == 'vote':
      #print(request.form)
      for k,v in request.form.items():
        if k.split('-')[0] in ['charRarity', 'charApprove']:
          if k.split('-')[0] == 'charRarity':
            voteType = 'rarity_votes'
          else:
            voteType = 'approval_votes'
          char_ind = int(k.split('-')[1])
          option = v.split('-')[1]
          db['proposed_characters'][char_ind][voteType][current_user.id] = option


      flash('Voted')

  proposed_characters = [(str(i), c) for i,c in enumerate(db['proposed_characters']) if c['status']=='pending']

  return render_template('characters/proposal.html', user = current_user, proposed_characters = proposed_characters)