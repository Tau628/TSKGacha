from flask import Blueprint, render_template, redirect, url_for
from replit import db, database
from flask_login import current_user

playersBP = Blueprint('playersBP', __name__, url_prefix='/players')


@playersBP.route('/<ply_ind>')
def player_page(ply_ind):
  if current_user.is_authenticated:
    return render_template('players/player_page.html', user = current_user, player = (ply_ind, database.to_primitive(db['players'][ply_ind])))
  else:
    return redirect(url_for('home'))

@playersBP.route('/')
def players():
  if current_user.is_authenticated:
    player_names = db['players'].keys()
    return render_template('players/players.html', user = current_user, player_names = [(url_for('playersBP.player_page', ply_ind = name), name) for name in player_names])
  else:
    return redirect(url_for('home'))

