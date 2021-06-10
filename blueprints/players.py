import datetime
import time

import pytz

from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db, database
from flask_login import current_user

playersBP = Blueprint('playersBP', __name__, url_prefix='/players')

est = pytz.timezone('US/Eastern')

@playersBP.route('/<ply_ind>', methods=['GET','POST'])
def player_page(ply_ind):

  if request.method == 'POST':
    last_check_in = db['players'][current_user.id]['last_check_in']
    now = int(time.time())

    prev = datetime.datetime.utcfromtimestamp(last_check_in)
    prev = est.localize(prev)
    curr = datetime.datetime.utcfromtimestamp(now)
    curr = est.localize(curr)

    diff = (curr.date()-prev.date()).days

    db['players'][current_user.id]['last_check_in'] = now
    db['players'][current_user.id]['coins'] += diff

    flash(f'You have redeemed {diff} Koins.', category='success')

  if current_user.is_authenticated:
    owned_characters = [(char_id, db['characters'][char_id]) for char_id in db['players'][ply_ind]['roster']]

    last_check_in = db['players'][current_user.id]['last_check_in']
    check_in = datetime.datetime.utcfromtimestamp(last_check_in)
    check_in = est.localize(check_in)
    check_in_string = check_in.strftime("%a, %b %d, %Y %I:%M %Z%z")
    #print(check_in.strftime("%Y-%m-%d %H:%M:%S %Z%z"))  

    return render_template('players/player_page.html', user = current_user, player = (ply_ind, database.to_primitive(db['players'][ply_ind])), owned_characters = owned_characters, check_in = check_in_string)
  else:
    return redirect(url_for('otherBP.home'))

@playersBP.route('/')
def players():
  if current_user.is_authenticated:
    player_names = db['players'].keys()
    return render_template('players/players.html', user = current_user, player_names = [(url_for('playersBP.player_page', ply_ind = name), name) for name in player_names])
  else:
    return redirect(url_for('otherBP.home'))

