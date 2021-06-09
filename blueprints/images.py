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


@imagesBP.route('/art/<arttype>/<charID>-<artID>.png')
def characterArt(arttype, charID, artID):

  if arttype == 'regular':
    size = (1106, 1482)
  elif arttype == 'mini':
    size = (742, 786)
  else:
    return

  character = db['characters'][charID]
  name = character['name']
  rarity = character['rarity']
  art = character['images'][int(artID)]
  url = art['url']
  crop = tuple(art['portrait'])

  img = Image.new('RGB', size)
  artwork = Image.open(requests.get(url, stream=True).raw)
  border = Image.open(f"images/{arttype}_frames/rarity{rarity}.png")

  if arttype == 'mini':
    artwork = artwork.crop(crop)

  artwork = artwork.resize(size)
  img.paste(artwork, (0,0))
  img.paste(border, (0,0), mask=border)
  
  if arttype == 'regular':
    title_font = ImageFont.truetype('comic.ttf', 100)
    title_text = name
    draw = ImageDraw.Draw(img)
    draw.text((450,1350), title_text, (0, 0, 0), font=title_font)

  return serve_pil_image(img)

@imagesBP.route('/imageTesting')
def imageTesting():
  return render_template('imageTesting.html', user=current_user)