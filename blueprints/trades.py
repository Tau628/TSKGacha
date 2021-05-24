from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db, database
from flask_login import current_user

tradesBP = Blueprint('tradesBP', __name__)

@tradesBP.route('/trades', methods=['GET','POST'])
def trades():
  roster = db['players'][current_user.id]['roster']
  roster = [(i, db['characters'][i]) for i in roster]

  other_players = {name:player for name,player in db['players'].items() if name!=current_user.id}

  if request.method == 'POST':
    print(request.form)
    
    offer_char = request.form.getlist('offer_character')
    partner = request.form.get('partner')
    request_char = request.form.get('request_character').split()
    offer_coins = int(request.form.get('offer_coins'))

    print(offer_char)

    trade = {
      'giving': offer_char,
      'instigator': current_user.id,
      'partner': partner,
      'receiving': request_char,
      'status': 'pending',
      'coins': offer_coins
    }

    db['trades'].append(trade)

    print(trade)

  return render_template('trades/trades.html', user=current_user, user_roster=roster, other_players=other_players)