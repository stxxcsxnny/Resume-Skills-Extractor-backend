from fastapi import FastAPI
from .routes.api import router
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Resume Skills Extractor",
    version="v1"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origins=["https://rsextractor.netlify.app"]

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Include routes
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "Hello World from FastAPI!",
        "app_name": os.getenv("APP_NAME", "Resume Skills Extractor"),
        "version": os.getenv("API_VERSION", "v1")
    } 