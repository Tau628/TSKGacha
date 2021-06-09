from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db, database
from flask_login import current_user

charactersBP = Blueprint('charactersBP', __name__, url_prefix='/characters')

from .pull import getListOwnedChars

@charactersBP.route('/<chr_ind>')
def character_page(chr_ind):
  if current_user.is_authenticated:
    
    #Determines if a characer is owned
    owned = getListOwnedChars()
    if chr_ind in owned:
      owner = owned[chr_ind]
    else:
      owner = None

    character = database.to_primitive(db['characters'][chr_ind])
    rarity = db['rarity_names'][str(character['rarity'])]
    rarity += " " + "☆"*character['rarity']

    return render_template('characters/character_page.html', user = current_user, character = character, chr_ind = chr_ind, owner=owner, rarity = rarity)
  
  else:
    return redirect(url_for('otherBP.home'))

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