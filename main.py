#!/bin/env python
from whiteboard import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=False, port=10000, host='0.0.0.0')
