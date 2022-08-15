from config.sql import note_sql
from model.database import DBconnect
from pydantic import BaseModel
from typing import Union
import time
import sys

current_milli_time = lambda: int(round(time.time() * 1000))

class Note(BaseModel):
    id: Union[str, None] = None
    title: Union[str, None] = None
    content: Union[str, None] = None

def get_notes():
    db_connect = DBconnect(sys.platform, 'WLS')
    desc, data = db_connect.query(note_sql.get('get_notes'))
    notes = []
    for row in data:
        notes.append(
            Note(
                id=row.id,
                title=None if not row.title else row.title.strip(),
                content=None if not row.content else row.content.strip()
            )
        )
    return notes

def create_note(form_data):
    data = [[current_milli_time(), form_data.title, form_data.content]]
    db_connect = DBconnect(sys.platform, 'WLS')
    db_connect.insert(note_sql.get('create_note'), data)

def update_note(form_data):
    data = [[form_data.id, form_data.title, form_data.content]]
    db_connect = DBconnect(sys.platform, 'WLS')
    db_connect.delete(note_sql.get('delete_note').format(form_data.id))
    db_connect.insert(note_sql.get('create_note'), data)

def delete_note(id):
    db_connect = DBconnect(sys.platform, 'WLS')
    db_connect.delete(note_sql.get('delete_note').format(id))