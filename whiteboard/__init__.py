from flask import Flask
from flask_socketio import SocketIO
from .database import db_wrapper
import logging.config
logging.config.fileConfig('logger.conf')
socketio = SocketIO(engineio_logger=True, cors_allowed_origins="*")
from . import events

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py', silent=True)

    db_wrapper.init_app(app)
    socketio.init_app(app)

    return app
