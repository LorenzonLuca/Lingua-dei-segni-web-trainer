import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from db.database import init_database, init_db_values
from api.routes import create_routes
from models.Logger import Logger
from models.HandRecognizer import HandRecognizer
from sockets.manager import get_socket_manager

load_dotenv()
app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, origins="*")

PORT=os.getenv('PORT')
ADMIN_PSW = os.getenv('ADMIN_PSW')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CONNECTION')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger = Logger(app)
logger.info(f"Start setup application")
db = init_database(app, logger)

with app.app_context():
    db.create_all()
    init_db_values(ADMIN_PSW)

hr = HandRecognizer(logger)

create_routes(app, db, logger, hr)

socket_app = get_socket_manager(app, db, logger, hr)

if __name__ == "__main__":
    logger.info(f"Application started on port {PORT}")
    socket_app.run(app, host='0.0.0.0', port=PORT, debug=True, ssl_context=('./../signlanguage.crt', './../signlanguage-privateKey.key'))