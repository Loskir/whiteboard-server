from flask import Flask
from flask_socketio import SocketIO
from .database import db_wrapper, Board, Stroke
import logging.config
logging.config.fileConfig('logger.conf')
socketio = SocketIO(engineio_logger=True, cors_allowed_origins="*")
from . import events

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py', silent=True)

    @app.route('/hello')
    def index():
        return 'Hello world!'

    db_wrapper.init_app(app)
    db_wrapper.database.create_tables([Board, Stroke])
    db_wrapper.database.close()

    socketio.init_app(app)
    return app
