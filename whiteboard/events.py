from . import socketio
from flask import request, current_app
from flask_socketio import emit, join_room
from .database import Board, Stroke, uses_db

app = current_app

@socketio.on('connect')
@uses_db
def on_connect():
    board_id = request.args.get('board', None)
    board = Board.get_or_none(board_id=board_id)
    if board is not None:
        app.logger.info(f'{request.sid} connected to {board_id}')
        join_room(board_id)
        strokes = list(board.strokes.dicts())
        for stroke in strokes:
            stroke.pop('board', None)
            stroke.pop('created_at', None)
        emit('update', {'add': strokes, 'delete': [], 'update': []})
    else:
        app.logger.info(f'{board_id} board does not exist, refusing connection')
        raise ConnectionRefusedError('Board does not exist')

@socketio.on('update')
@uses_db
def on_update(data: dict):
    app.logger.info(str({x: f'{len(data[x])} stroke(s)' for x in data}))
    board_id = request.args.get('board')
    board = Board.get_or_none(board_id=board_id)
    if board is not None:
        for raw_stroke in data.get('add', []):
            Stroke.create(board=board, **raw_stroke)
        for raw_stroke in data.get('delete', []):
            stroke = Stroke.get_or_none(stroke_id=raw_stroke.get('stroke_id'))
            if stroke is not None:
                stroke.delete_instance()
        for raw_stroke in data.get('update', []):
            content = raw_stroke.get('content', None)
            if content is not None:
                stroke = Stroke.get_or_none(stroke_id=raw_stroke.get('stroke_id'))
                if stroke is not None:
                    stroke.content = content
                    stroke.save()

        emit('update', data, room=board_id, include_self=False) #TODO: check validity
    else:
        emit('error', {'error': 'Board does not exist'})
