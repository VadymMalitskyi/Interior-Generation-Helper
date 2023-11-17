import subprocess
import time

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel

app = FastAPI()

class GenerationConfig(BaseModel):
    style: str
    room_id: str
    required_objects: str
    room_type: str

@app.post("/generate_bedroom")
def generate_room(generation_config: GenerationConfig):  # file: UploadFile = File(...)
    try:
        if generation_config.room_type == "bedroom":
            weights_path = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/trained_models/L1F6VFKD0/model_01000"
        else:
            weights_path = None # TODO: add weights for living room

        file_name = str(int(time.time()))
        script_name = '/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/scripts/generate_scenes.py'

        command = [
            'python',
            script_name,
            "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/config/bedrooms_config.yaml",
            "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/visualizations",
            "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/data/pickle_data/threed_future_model_bedroom.pkl",
            "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/demo/floor_plan_texture_images",
            "--weight_file", weights_path,
            "--n_sequences", "1",
            "--without_screen",
            "--scene_id", generation_config.room_id,
            "--file_save_name", file_name,
            "--required_style", generation_config.style,
            "--required_objects", generation_config.required_objects,
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

