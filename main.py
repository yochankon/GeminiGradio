from fastapi import FastAPI
from app_test4 import get_gemini_response
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, port=9500, host='0.0.0.0', reload= True)
