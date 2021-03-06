from flask import Flask

from blueprints.players import playersBP
from blueprints.characters import charactersBP
from blueprints.auth import authBP, login_manager
from blueprints.pull import pullBP
from blueprints.other import otherBP
from blueprints.trades import tradesBP
from blueprints.images import imagesBP

app = Flask(__name__)
login_manager.init_app(app)
app.register_blueprint(playersBP)
app.register_blueprint(charactersBP)
app.register_blueprint(authBP)
app.register_blueprint(pullBP)
app.register_blueprint(otherBP)
app.register_blueprint(tradesBP)
app.register_blueprint(imagesBP)

if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(host='0.0.0.0', port=8080, debug=True)