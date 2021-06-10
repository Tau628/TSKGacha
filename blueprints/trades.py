from flask import Blueprint, render_template, request, flash
from replit import db
from flask_login import current_user

tradesBP = Blueprint('tradesBP', __name__)

@tradesBP.route('/trades', methods=['GET','POST'])
def trades():

  if request.method == 'POST':
    button = request.form.get('submit_button')
    print(request.form)
    
    if button == 'offer':
      #Gets all of the information from the form   
      offer_char = request.form.getlist('offer_character')
      partner = request.form.get('partner')
      request_char = request.form.get('request_character').split() #TODO: This should be changed to get list later, once the dynamic dropdown is implemented
      offer_coins = int(request.form.get('offer_coins'))

      #Error catching
      if offer_char == []:
        flash('Please select at least one character to offer.', category='error')
      elif partner is None:
        flash('Please specify a player to trade with.', category='error')
      elif len(offer_char)!=len(request_char):
        flash("Please offer the same number of characters that you're requesting.", category='error')

      #If no errors are found...
      else:
        #Sets up dictionary that will contain all of the trade information
        trade = {
          'giving': offer_char,
          'instigator': current_user.id,
          'partner': partner,
          'receiving': request_char,
          'status': 'pending',
          'coins': offer_coins
        }

        #And appends it to the trade database
        db['trades'].append(trade)

    #If a trade was revoded, change it's status
    elif button.split('-')[0] == 'revoke':
      trade_id = int(button.split('-')[1])
      db['trades'][trade_id]['status'] = 'revoked'
      flash('Trade revoked.', category='success')

    #If a trade was rejected, change it's status
    elif button.split('-')[0] == 'reject':
      trade_id = int(button.split('-')[1])
      db['trades'][trade_id]['status'] = 'rejected'
      flash('Trade rejected.', category='success')

    #If a trade was accepted...
    elif button.split('-')[0] == 'accept':
      trade_id = int(button.split('-')[1])

      #Get the trade information
      trade = db['trades'][trade_id]

      #Error catching
      if trade['status']!='pending':
        flash('This is no longer a valid trade.', category='error')

      elif trade['partner'] != current_user.id:
        flash('You are not authorized for this trade. Trade deleted.', category='error')
        db['trades'][trade_id]['status'] = 'errored'

      elif not set(trade['receiving']).issubset(set(db['players'][current_user.id]['roster'])):
        flash("You don't have the characters for this trade. Trade deleted.", category='error')
        db['trades'][trade_id]['status'] = 'errored'

      elif not set(trade['giving']).issubset(set(db['players'][trade['instigator']]['roster'])):
        flash(f"{trade['instigator']} doesn't have the characters for this trade. Trade deleted.", category='error')
        db['trades'][trade_id]['status'] = 'errored'

      elif 0 < -trade['coins'] > db['players'][current_user.id]['coins']:
        flash("You don't have enough coins.", category='error')

      elif 0 < trade['coins'] > db['players'][trade['instigator']]['coins']:
        flash(f"{trade['instigator']} don't have enough coins.", category='error')

      #If no errors found...
      else:
        #Add the characters to the players rosters
        for char in trade['giving']:
          print(f"Adding {char} to {current_user.id}")
          db['players'][current_user.id]['roster'].append(char)
        for char in trade['receiving']:
          print(f"Adding {char} to {trade['instigator']}")
          db['players'][trade['instigator']]['roster'].append(char)

        #Remove the characters from the players rosters
        for char in trade['giving']:
          print(f"Deleting {char} from {trade['instigator']}")
          db['players'][trade['instigator']]['roster'].remove(char)
        for char in trade['receiving']:
          print(f"Deleting {char} from {current_user.id}")
          db['players'][current_user.id]['roster'].remove(char)

        #Transfer coins between players
        db['players'][current_user.id]['coins'] += trade['coins']
        db['players'][trade['instigator']]['coins'] -= trade['coins']

        #Change status of trade
        db['trades'][trade_id]['status'] = 'accepted'

        #Flash message to the user
        flash('Trade accepted!', category='success')

  #End of POST logic

  #Get the current players roster
  roster = db['players'][current_user.id]['roster']
  roster = [(i, db['characters'][i]) for i in roster]

  #Gets a list of other players
  other_players = {name:player for name,player in db['players'].items() if name!=current_user.id}
  
  #Gets a list of current pending trades 
  curr_trades = [(i,trade) for i, trade in enumerate(db['trades']) if trade['status']=='pending']

  #Filters the list to be only your trades
  your_trades = [(i,trade) for i, trade in curr_trades if trade['instigator']==current_user.id]

  #Looks for trades offered to you
  my_trades = [(i,trade) for i, trade in curr_trades if trade['partner']==current_user.id]

  #Returns HTML template
  return render_template('trades/trades.html', user=current_user, user_roster=roster, other_players=other_players, trades = {'your':your_trades, 'my':my_trades}, characters=db['characters'])