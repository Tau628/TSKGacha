import json
from replit import db, database

def recurse_prim(x):
  x = database.to_primitive(x)
  if isinstance(x, dict):
    return {k:recurse_prim(v) for k,v in x.items()}
  if isinstance(x,list):
    return [recurse_prim(y) for y in x]
  return x


#Loads in database from JSON
def loadDatabase(filename):
  for k in db.keys():
    del db[k]
  with open(f'./{filename}') as f:
    data = json.load(f)
  for k, v in data.items():
    db[k] = v

#Saves database to JSON
def saveDatabase(filename):
  data = {k:recurse_prim(v) for k,v in db.items()}
  with open(filename, "w") as outfile: 
      json.dump(data, outfile, sort_keys=True, indent=4)


def loadArtwork():
  with open(f'./TEMP.json') as f:
    data = json.load(f)

  for name, art in data.items():

    for k,v in db['characters'].items():
      if v['name'] == name:
        db['characters'][k]['images'] = [
          {'NSFW': False, 'portrait': None, 'url': art}
        ]
        break

def loadDescriptions():
  with open(f'./TEMP.json') as f:
    data = json.load(f)

  for name, desc in data.items():

    for k,v in db['characters'].items():
      if v['name'] == name:
        db['characters'][k]['description'] = desc
        break

print('Start')

saveDatabase('sample.json')

print('Done')