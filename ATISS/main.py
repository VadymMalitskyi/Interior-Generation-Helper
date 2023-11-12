import subprocess
import time

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()


@app.get("/generate_room")
def generate_room():  # file: UploadFile = File(...)
    try:
        file_name = str(int(time.time()))
        script_name = '/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/scripts/generate_scenes.py'

        command = [
            'python',
            script_name,
            "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/config/bedrooms_config.yaml",
            "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/visualizations",
            "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/data/pickle_data/threed_future_model_bedroom.pkl",
            "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/demo/floor_plan_texture_images",
            "--weight_file", "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/trained_models/L1F6VFKD0/model_01000",
            "--n_sequences", "1",
            "--without_screen",
            "--file_save_name", file_name,
        ]

        # Run the script with subprocess
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")
        return HTTPException(status_code=500, detail="Error running the script")
    except Exception as e:
        print(f"An error occurred: {e}")
        return HTTPException(status_code=500, detail="An error occurred")

    file_path = Path(f"/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/visualizations/{file_name}.glb")
    return FileResponse(file_path, filename=file_path.name)

