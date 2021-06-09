from PIL import Image, ImageFont, ImageDraw 
import requests
from io import BytesIO

from flask import Blueprint, render_template, send_file#, redirect, url_for, request, flash
from flask_login import current_user
from replit import db

imagesBP = Blueprint('imagesBP', __name__)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


@imagesBP.route('/art/<charID>-<artID>.png')
def characterArt(charID, artID):
  #Blank canvas
  img = Image.new('RGB', (1106, 1482))
  
  url = db['characters'][charID]['image'][int(artID)]['url']
  
  art = Image.open(requests.get(url, stream=True).raw)
  border = Image.open("images/Nonplussed_Frame.png")

  art = art.resize((1106, 1482))
  img.paste(art, (0,0))
  img.paste(border, (0,0), mask=border)
  title_font = ImageFont.truetype('comic.ttf', 100)
  title_text = "Shantae"
  draw = ImageDraw.Draw(img)
  draw.text((450,1350), title_text, (0, 0, 0), font=title_font)

  return serve_pil_image(img)

@imagesBP.route('/art/mini/<charID>-<artID>.png')
def characterArtMini(charID, artID):
  img = Image.new('RGB', (742, 786))
  url = db['characters'][charID]['image'][int(artID)]['url']
  crop = tuple(db['characters'][charID]['image'][int(artID)]['portrait'])
  art = Image.open(requests.get(url, stream=True).raw)
  art = art.crop(tuple(crop))
  border = Image.open("images/Nonplussed_mini.png")

  art = art.resize((742, 786))
  img.paste(art, (0,0))
  img.paste(border, (0,0), mask=border)

  return serve_pil_image(img)

@imagesBP.route('/imageTesting')
def imageTesting():
  return render_template('imageTesting.html', user=current_user)