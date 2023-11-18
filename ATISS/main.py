import subprocess
import time
import io
import pickle
import random

import numpy as np
from PIL import Image

from fastapi import FastAPI, File, HTTPException, Form
from fastapi.responses import FileResponse
from pathlib import Path
from typing_extensions import Annotated

app = FastAPI()

bedroom_saved_info = {
    "images_path": "/home/vadym_wsl/projects/Interior-Generation-Helper/images_list.pkl",
    "names_path": "/home/vadym_wsl/projects/Interior-Generation-Helper/names_list.pkl",
}
livingroom_saved_info = {  # TODO: fill later
    "images_path": "",
    "names_path": "",
}

def get_room_id(image_arr: np.ndarray, room_type: str) -> str:
    existing_rooms_info = bedroom_saved_info if room_type == "bedroom" else livingroom_saved_info
    with open(existing_rooms_info["images_path"], "rb") as f:
        images = pickle.load(f)

    with open(existing_rooms_info["names_path"], "rb") as f:
        names = pickle.load(f)
    
    for image, name in zip(images, names):
        print(image.shape)
        print(image)
        if np.array_equal(image, image_arr):
            print("Found image id: ", name)
            return name
    print("Image id not found")
    return random.sample(names, 1)[0]

@app.post("/generate_room")
def generate_room(
    room_layout: Annotated[bytes, File()],
    style: Annotated[str, Form()],
    room_type: Annotated[str, Form()],
    required_objects: Annotated[str, Form()],
    layout_width: Annotated[int, Form()],
    layout_height: Annotated[int, Form()],
):
    try:
        layout_image = Image.frombytes("RGB", (layout_width, layout_height), io.BytesIO(room_layout).read())
        room_id = get_room_id(image_arr=np.array(layout_image), room_type=room_type)
        print("Image shape: ", np.array(layout_image).shape)
        if room_type == "bedroom":
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
            "--scene_id", room_id,
            "--file_save_name", file_name,
            "--required_style", style,
            "--required_objects", required_objects,
        ]

        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")
        return HTTPException(status_code=500, detail="Error running the script")
    except Exception as e:
        print(f"An error occurred: {e}")
        return HTTPException(status_code=500, detail="An error occurred")

    file_path = Path(f"/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/visualizations/{file_name}.glb")
    return FileResponse(file_path, filename=file_path.name)

