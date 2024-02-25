import os
from flask import Flask
from dotenv import load_dotenv
from flask_session import Session
load_dotenv()

from routes_bp import routes_bp
from utilities.errors import errors

app = Flask(__name__)


app.secret_key = os.getenv('APP_SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
sess = Session()
sess.init_app(app)

app.register_blueprint(routes_bp)
app.register_blueprint(errors)

if not os.path.isdir(os.getenv('FACES_DIR')): os.makedirs(os.getenv('FACES_DIR'))


if __name__ == '__main__':
    app.run(debug=True)
