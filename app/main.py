import uvicorn
from fastapi import FastAPI
from app.utils import replace, remove_stops
from app.router import g_router
from app import database as db



# Create app
app = FastAPI()
app.include_router(g_router)

db.create_bd()

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
