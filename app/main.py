import uvicorn
from fastapi import FastAPI
from app.routers.genre_router import router as g_router
# Load the model


# Create app
app = FastAPI()
app.include_router(g_router)



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
