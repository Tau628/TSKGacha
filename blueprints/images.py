from PIL import Image, ImageFont, ImageDraw 
import requests
from io import BytesIO

from flask import Blueprint, render_template, send_file
from flask_login import current_user
from replit import db

imagesBP = Blueprint('imagesBP', __name__)

#Converts a PIL image object to something that Flask can serve.
def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

#Generates artwork for a charater with titles and borders
@imagesBP.route('/art/<arttype>/<charID>-<artID>.png')
def characterArt(arttype, charID, artID):

  if arttype == 'regular':
    size = (1106, 1482)
  elif arttype == 'mini':
    size = (665, 691)
  else:
    return

  #Gets all the necessary data
  character = db['characters'][charID]
  name = character['name']
  rarity = character['rarity']
  art = character['images'][int(artID)]
  url = art['url']
  crop = art['portrait']
  nsfw = art['NSFW']
  
  #Determines if NSFW art can be displayed
  if current_user.is_authenticated:
    allow_nsfw = db['players'][current_user.id]['NSFW_shown']
  else:
    allow_nsfw = False

  #Gets all of the images that it's going to work with
  img = Image.new('RGB', size)

  if nsfw and not allow_nsfw:
    artwork = Image.new('RGB', size)
    crop = None
  else:
    artwork = Image.open(requests.get(url, stream=True).raw)
    
  border = Image.open(f"images/{arttype}_frames/rarity{rarity}.png")

  #If it's a mini art, crop the image
  if arttype == 'mini' and crop is not None:
    artwork = artwork.crop(tuple(crop))

  #Scale the artwork to the correct size and combine the artwork and the frame
  artwork = artwork.resize(size)
  img.paste(artwork, (0,0))
  img.paste(border, (0,0), mask=border)
  
  #If it's a regular art, add the name of the character
  if arttype == 'regular':
    text_size = 100
    title_font = ImageFont.truetype('fonts/broadway.ttf', text_size)
    
    while(title_font.getsize(name)[0] > 530):
      text_size -= 5
      title_font = ImageFont.truetype('fonts/broadway.ttf', text_size)

    title_text = name
    draw = ImageDraw.Draw(img)
    draw.text((450,1370+(95-title_font.getsize(name)[1])/2), title_text, (0, 0, 0), font=title_font)

  if arttype == 'mini':
    img = img.resize((100,100))

  return serve_pil_image(img)