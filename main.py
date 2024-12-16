from fastapi import FastAPI
from routes.routes import endPoints

app = FastAPI()
app.include_router(endPoints)