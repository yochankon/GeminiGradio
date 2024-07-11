from fastapi import FastAPI
from app_test4 import get_gemini_response

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
