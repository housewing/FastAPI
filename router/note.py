from fastapi import APIRouter
from model.note import Note, get_notes, create_note, update_note, delete_note

router = APIRouter()

@router.get('/getNotes')
async def getNotes():
    return get_notes()

@router.post('/createNote')
async def createNote(form_data: Note):
    if not form_data.id:
        create_note(form_data)
        return {'message': 'create note finish'}
    return {'message': 'create note fail'}

@router.post('/updateNote')
async def updateNote(form_data: Note):
    if form_data.id:
        update_note(form_data)
        return {'message': 'update note finish'}
    return {'message': 'update note fail'}

@router.post('/deleteNote')
async def deleteNote(form_data: Note):
    if form_data.id:
        delete_note(form_data.id)
        return {'message': 'delete note finish'}
    return {'message': 'delete note fail'}