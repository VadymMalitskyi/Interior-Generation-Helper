from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Path to the file you want to serve for download
file_path = Path("/home/vadym_wsl/projects/Interior-Generation-Helper/web_app/sample_file.glb")


@app.get("/download")
def download_file():
    return FileResponse(file_path, filename=file_path.name)
