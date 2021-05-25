from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db, database
from flask_login import current_user

tradesBP = Blueprint('tradesBP', __name__)

@tradesBP.route('/trades', methods=['GET','POST'])
def trades():

  if request.method == 'POST':
    button = request.form.get('submit_button')
    print(request.form)
    
    if button == 'offer':       
      offer_char = request.form.getlist('offer_character')
      partner = request.form.get('partner')
      request_char = request.form.get('request_character').split() #TODO: This should be changed to get list later
      offer_coins = int(request.form.get('offer_coins'))

      print(partner)

      if offer_char == []:
        flash('Please select at least one character to offer.', category='error')
      elif partner is None:
        flash('Please specify a player to trade with.', category='error')
      elif len(offer_char)!=len(request_char):
        flash("Please offer the same number of characters that you're requesting.", category='error')

      else:
        trade = {
          'giving': offer_char,
          'instigator': current_user.id,
          'partner': partner,
          'receiving': request_char,
          'status': 'pending',
          'coins': offer_coins
        }

        db['trades'].append(trade)


  roster = db['players'][current_user.id]['roster']
  roster = [(i, db['characters'][i]) for i in roster]

  other_players = {name:player for name,player in db['players'].items() if name!=current_user.id}

  curr_trades = [(i,trade) for i, trade in enumerate(db['trades']) if trade['status']=='pending']
  your_trades = [(i,trade) for i, trade in curr_trades if trade['instigator']==current_user.id]
  my_trades = [(i,trade) for i, trade in curr_trades if trade['partner']==current_user.id]

  return render_template('trades/trades.html', user=current_user, user_roster=roster, other_players=other_players, trades = {'your':your_trades, 'my':my_trades}, characters=db['characters'])