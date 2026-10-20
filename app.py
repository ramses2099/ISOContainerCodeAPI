from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}