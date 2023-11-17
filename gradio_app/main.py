import gradio as gr
import os
import json
import requests
import time
import hashlib
import random

import numpy as np
from PIL import Image


bedroom_objects = ["armchair", "bookshelf", "cabinet", "ceiling_lamp", "chair", "children_cabinet",
                   "coffee_table", "desk", "double_bed", "dressing_chair", "dressing_table", "kids_bed",
                   "nightstand", "pendant_lamp", "shelf", "single_bed", "sofa", "stool", "table",
                   "tv_stand", "wardrobe"]

bedroom_hash_to_room = {
    "a700a745063abfb9cd01b37f9c63ef68fc578b78304bc8f16b939373218e3339": "SecondBedroom-18509",
    "1dda516350c4f74caf1f24342680932b5b4f4ae1247fe03c9cb31fd0b25173c3": "MasterBedroom-2888",
    "1fe1977cc02f6de5447e614540001e7a0c380d73779c833fe580eb5097d43d83": "SecondBedroom-60495",
    "6a1853f2b4d90244a12ce11cf61944a4e6c87c237b13ad3f31b27e6e05075631": "MasterBedroom-29735",
    "d51baebb753c66f156246cbb063ddfba5c7b9c9216b93ced6bb580f29f889ead": "MasterBedroom-81302",
}

livingroom_hash_to_room = {  # TODO: add living room hashes
}

# Function to download and save the 3D model
def download_3d_model(save_path, style, room_type, room_id, objects):
    json = {"style": style, "room_id": room_id, "room_type": room_type, "required_objects": objects}
    response = requests.post("http://127.0.0.1:8000/generate_room", json=json)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

# Gradio interface function
def visualize_3d_model(room_layout, room_type, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand):
    shape = room_layout.shape
    tuple_list = []

    # Iterate through the array and convert it to a tuple of tuples
    for i in range(shape[0]):
        for j in range(shape[1]):
            tuple_list.append(tuple(room_layout[i, j]))

    # Convert the list of tuples to a tuple
    result_tuple = tuple(tuple_list)
    h = hashlib.new('sha256')#sha256 can be replaced with diffrent algorithms
    h.update(str(result_tuple).encode()) #give a encoded string. Makes the String to the Hash 
    passed_img_hash = h.hexdigest().strip()#Prints the Hash
    print("Passed image hash:", passed_img_hash)
    
    img_hash_to_room = livingroom_hash_to_room
    if room_type == "bedroom":
        img_hash_to_room = bedroom_hash_to_room

    if img_hash_to_room.get(passed_img_hash) is None:
        print("No such room in the database. Choosing random one.")
        _, room_id = random.choice(list(img_hash_to_room.items()))
    else:
        print("Room found in the database.")
        room_id = img_hash_to_room[passed_img_hash]
    print(f"Style: {style}")

    objects_dict = {
        "double_bed": n_double_bed,
        "wardrobe": n_wardrobe,
        "pendant_lamp": n_pendant_lamp,
        "ceiling_lamp": n_ceiling_lamp,
        "tv_stand": n_tv_stand,
        "nightstand": n_nightstand
    }
    objects_str = json.dumps(objects_dict)
    print(f"Objects: {objects_str}")

    filepath = f"created_models/{int(time.time())}.glb"
    if download_3d_model(save_path=filepath, style=style, room_type=room_type, room_id=room_id, objects=objects_str):
        return gr.Model3D(filepath)
    else:
        return "Failed to download 3D model."


with gr.Blocks() as demo:
    gr.Markdown('<h1 style="text-align: center;"> 3D Rooms Generator</h1>')
    with gr.Tab("Bedroom"):
        room_type = "bedroom"
        with gr.Column():
            room_layout = gr.Image()
            style = gr.Dropdown(['Light Luxury', 'Modern', 'Japanese', 
                        'Southeast Asia', 'Nordic', 'Korean', 
                        'Mediterranean', 'New Chinese', 'Vintage/Retro', 
                        'Neoclassical', 'American Country', 
                        'Ming Qing', 'Minimalist', 'Industrial', 'No style'], value="No style", label="Style")
            with gr.Accordion("Set objects"):
                n_double_bed = gr.Slider(-1, 5, step=1, label="double_bed")
                n_wardrobe = gr.Slider(-1, 5, step=1, label="wardrobe")
                n_pendant_lamp = gr.Slider(-1, 5, step=1, label="pendant_lamp")
                n_ceiling_lamp = gr.Slider(-1, 5, step=1, label="ceiling_lamp")
                n_tv_stand = gr.Slider(-1, 5, step=1, label="tv_stand")
                n_nightstand = gr.Slider(-1, 5, step=1, label="nightstand")
        with gr.Column():
            output_model = gr.Model3D()
        
        generate_bedroom_button = gr.Button("Generate Bedroom")

    with gr.Tab("Living Room") as room_type:
        room_type = "living_room"
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Flip")

        generate_living_room_button = gr.Button("Generate Living Room")

    generate_bedroom_button.click(visualize_3d_model, inputs=[room_layout, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand], outputs=output_model)
    generate_living_room_button.click(visualize_3d_model, inputs=[room_layout, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand], outputs=output_model)

if __name__ == "__main__":
    demo.launch(share=True)