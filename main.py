from flask import Flask
from flask_cors import CORS

from common.config import PORT
from app.api.routes import routes

app = Flask(__name__)

CORS(app)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=PORT)
