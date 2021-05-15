import peewee as pw
import uuid
import time
from playhouse.flask_utils import FlaskDB
import functools

db_wrapper = FlaskDB()


class LongTextField(pw.TextField):
    field_type = 'LONGTEXT'


class Board(db_wrapper.Model):
    board_id = pw.CharField(unique=True, index=True)
    created_at = pw.IntegerField(default=time.time)


class Stroke(db_wrapper.Model):
    board = pw.ForeignKeyField(Board, backref='strokes')
    stroke_id = pw.CharField(default=lambda: str(uuid.uuid4()), unique=True, index=True)
    created_at = pw.IntegerField(default=time.time)
    content = LongTextField()


# SocketIO doesn't invoke before_request and after request
# so FlaskDB doesn't really work
def uses_db(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        db_wrapper.database.connect(reuse_if_open=False)
        try:
            return func(*args, **kwargs)
        finally:
            db_wrapper.close_db(None)
    return inner
