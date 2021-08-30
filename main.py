#!/bin/env python
from dotenv import load_dotenv
import os

from whiteboard import create_app, socketio

load_dotenv()

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=False, port=int(os.getenv('PORT', '10000')), host=os.getenv('HOST', '0.0.0.0'))
