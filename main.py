from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import auth, user, note

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(note.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home_page():
    return { 'result': 'this is homepage'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True, debug=True)
    # uvicorn main:app --host=127.0.0.1 --port=8000 --reload