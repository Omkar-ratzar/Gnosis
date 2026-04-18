from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import auth, search, upload
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(search.router, prefix="/api/search")
app.include_router(upload.router, prefix="/api/upload")

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

def serve_html(filename: str):
    return FileResponse(os.path.join(BASE_DIR, "static", filename))

@app.get("/")
def root():
    return serve_html("index.html")

@app.get("/upload")
def upload_page():
    return serve_html("upload.html")

@app.get("/search")
def search_page():
    return serve_html("search.html")

@app.get("/about")
def about_page():
    return serve_html("about.html")
