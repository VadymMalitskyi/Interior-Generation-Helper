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
    "images_path": "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/processed_layout_img/bedroom/images_list.pkl",
    "names_path": "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/processed_layout_img/bedroom/names_list.pkl",
}
livingroom_saved_info = {
    "images_path": "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/processed_layout_img/livingroom/images_list.pkl",
    "names_path": "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/processed_layout_img/livingroom/names_list.pkl",
}
diningroom_saved_info = {
    "images_path": "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/processed_layout_img/diningroom/images_list.pkl",
    "names_path": "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/processed_layout_img/diningroom/names_list.pkl",
}


def get_room_id(image_arr: np.ndarray, room_type: str) -> str:
    existing_rooms_info = bedroom_saved_info
    if room_type == "livingroom":
        existing_rooms_info = livingroom_saved_info
    elif room_type == "diningroom":
        existing_rooms_info = diningroom_saved_info
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
        layout_image = Image.frombytes(
            "RGB", (layout_width, layout_height), io.BytesIO(room_layout).read()
        )
        room_id = get_room_id(image_arr=np.array(layout_image), room_type=room_type)
        print("Image shape: ", np.array(layout_image).shape)
        if room_type == "bedroom":
            weights_path = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/trained_models/0ZTXKZJKD/model_03300"
            config_path = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/config/bedrooms_config.yaml"
            threed_model_path = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/data/pickle_data/threed_future_model_bedroom.pkl"
        elif room_type == "livingroom":
            weights_path = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/trained_models/DTPI0WWZE/model_04000"
            config_path = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/config/living_rooms_config.yaml"
            threed_model_path = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/data/pickle_data/threed_future_model_livingroom.pkl"
        else:
            weights_path = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/trained_models/SSLGRLG5N/model_03500"
            config_path = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/config/dining_rooms_config.yaml"
            threed_model_path = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/data/pickle_data/threed_future_model_diningroom.pkl"

        file_name = str(int(time.time()))
        script_name = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/scripts/generate_scenes.py"

        command = [
            "python",
            script_name,
            config_path,
            "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/visualizations",
            threed_model_path,
            "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/demo/floor_plan_texture_images",
            "--weight_file",
            weights_path,
            "--n_sequences",
            "1",
            "--without_screen",
            "--scene_id",
            room_id,
            "--file_save_name",
            file_name,
            "--required_style",
            style,
            "--required_objects",
            required_objects,
        ]

        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")
        return HTTPException(status_code=500, detail="Error running the script")
    except Exception as e:
        print(f"An error occurred: {e}")
        return HTTPException(status_code=500, detail="An error occurred")

    file_path = Path(
        f"/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/visualizations/{file_name}.glb"
    )
    return FileResponse(file_path, filename=file_path.name)
