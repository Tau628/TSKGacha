from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db, database
from flask_login import current_user

tradesBP = Blueprint('tradesBP', __name__)

@tradesBP.route('/trades', methods=['GET','POST'])
def trades():
  roster = db['players'][current_user.id]['roster']
  roster = [(i, db['characters'][i]) for i in roster]
  if request.method == 'POST':
    print('POST was done.')
    print(request.form)
    print(request.form.getlist('offer_character'))
  return render_template('trades/trades.html', user=current_user, user_roster=roster)