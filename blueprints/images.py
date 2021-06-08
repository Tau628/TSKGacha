from PIL import Image, ImageFont, ImageDraw 
import requests
from io import BytesIO

from flask import Blueprint, render_template, send_file#, redirect, url_for, request, flash
from flask_login import current_user

imagesBP = Blueprint('imagesBP', __name__)

#https://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


@imagesBP.route('/shantae.png')
def shantae():
  img = Image.new('RGB', (1106, 1482))
  url = r"https://cdn.discordapp.com/attachments/846922804074643467/851621760985727046/Shantae.png"
  art = Image.open(requests.get(url, stream=True).raw)
  border = Image.open("images/Nonplussed_Frame.png")

  print('img', img.size)
  print('art', art.size)
  print('border', border.size)

  art = art.resize((1106, 1482))
  img.paste(art, (0,0))
  img.paste(border, (0,0), mask=border)
  title_font = ImageFont.truetype('comic.ttf', 100)
  title_text = "Shantae"
  draw = ImageDraw.Draw(img)
  draw.text((450,1350), title_text, (0, 0, 0), font=title_font)



  return serve_pil_image(img)#render_template('imageTesting.html', user=current_user)

@imagesBP.route('/imageTesting')
def imageTesting():
  return render_template('imageTesting.html', user=current_user)