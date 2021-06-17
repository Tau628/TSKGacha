import datetime
import time

import pytz

from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db, database
from flask_login import current_user

playersBP = Blueprint('playersBP', __name__, url_prefix='/players')

from .pull import pullChar
est = pytz.timezone('US/Eastern')

#A player's main page
@playersBP.route('/<ply_ind>', methods=['GET','POST'])
def player_page(ply_ind):

  if request.method == 'POST':
    button = request.form.get('submit_button')

    #If a user is checking in to claim their coins
    if button == 'check-in':
      last_check_in = db['players'][current_user.id]['last_check_in']
      now = int(time.time())

      #Get's the previous check in time and the current time
      prev = datetime.datetime.utcfromtimestamp(last_check_in)
      prev = est.localize(prev)
      curr = datetime.datetime.utcfromtimestamp(now)
      curr = est.localize(curr)

      #Calculates the number of days since the last check in
      diff = (curr.date()-prev.date()).days

      #Adds the appropriate number of coins
      db['players'][current_user.id]['last_check_in'] = now
      db['players'][current_user.id]['coins'] += diff

      #Flashes success message to user
      flash(f'You have redeemed {diff} Koins.', category='success')
    
    #If a user is changing their NSFW status
    elif button.split('-')[0] == 'NSFW':
      toggle = button.split('-')[1] == 'on'
      db['players'][current_user.id]['NSFW_shown'] = toggle
      flash('Preferences updated. Please clear cache.', category='success')

    elif button == 'expand-roster':
      player = db['players'][ply_ind]
      roster_size = player['max_roster']

      if roster_size >= len(db['expansion_costs']):
        flash("You already have the max roster size.", category='error')
      else:
        cost = db['expansion_costs'][roster_size]
        
        if cost > player['coins']:
          flash("You don't have enough coins.", category='error')
        else:
          #Deducting the cost of the banner and adding to their roster
          db['players'][current_user.id]['max_roster'] += 1
          db['players'][current_user.id]['coins'] -= cost
          
          #Returns a page to show the user thier pull
          return pullChar(banner_name='base')

  if current_user.is_authenticated:

    player = db['players'][ply_ind]

    #Get a list of owned characters and wishlisted characters by the player
    owned_characters = [(char_id, db['characters'][char_id]) for char_id in player['roster']]
    wishlist_characters = [(char_id, db['characters'][char_id]) for char_id in player['wishlist']]

    #Gets the time that the player last checked in
    last_check_in = player['last_check_in']
    check_in = datetime.datetime.utcfromtimestamp(last_check_in)
    check_in = est.localize(check_in)
    check_in_string = check_in.strftime("%a, %b %d, %Y %I:%M %Z%z")

    #Returns the HTML template
    return render_template('players/player_page.html', user = current_user, player = (ply_ind, database.to_primitive(db['players'][ply_ind])), owned_characters = owned_characters, wishlist_characters=wishlist_characters, check_in = check_in_string)
  
  #If the user is not logged in, redirect to the home page.
  else:
    return redirect(url_for('otherBP.home'))

#Page to display all the players
@playersBP.route('/')
def players():
  if current_user.is_authenticated:
    #Gets a list of players to pass to the HTML template.
    player_names = db['players'].keys()
    return render_template('players/players.html', user = current_user, player_names = player_names)
  #If the user is not logged in, redirect to the home page.
  else:
    return redirect(url_for('otherBP.home'))

