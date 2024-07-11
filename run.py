from fastapi import FastAPI
import uvicorn

from gradio_app import app  # Import the FastAPI app instance from app.py

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9300)
