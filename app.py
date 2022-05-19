from flask import Flask
from flask_cors import CORS

import controllers.front_controller as fc


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

fc.route(app)

if __name__ == '__main__':
    app.run()
