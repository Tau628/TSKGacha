from flask import Blueprint, render_template, redirect, url_for, request, flash
from replit import db, database
from flask_login import current_user

pullBP = Blueprint('pullBP', __name__)

@pullBP.route('/pull')
def pull():
  return render_template('pull/pull.html', user = current_user)