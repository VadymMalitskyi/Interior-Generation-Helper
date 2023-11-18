import json
import requests
import time

import gradio as gr
from PIL import Image


bedroom_objects = ["armchair", "bookshelf", "cabinet", "ceiling_lamp", "chair", "children_cabinet",
                   "coffee_table", "desk", "double_bed", "dressing_chair", "dressing_table", "kids_bed",
                   "nightstand", "pendant_lamp", "shelf", "single_bed", "sofa", "stool", "table",
                   "tv_stand", "wardrobe"]
livingroom_objects = []  # TODO: fill later

def download_3d_model(save_path, style, room_type, objects, room_layout, layout_width, layout_height):
    json = {
        "style": style, 
        "room_type": room_type, 
        "required_objects": objects, 
        "layout_width": layout_width,
        "layout_height": layout_height,
    }
    response = requests.post(
        "http://127.0.0.1:8000/generate_room", 
        data=json, 
        files={"room_layout": room_layout}
    )
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def visualize_3d_bedroom(room_layout, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand):
    return visualize_3d_model(room_layout, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand, room_type="bedroom")

def visualize_3d_livingroom(room_layout, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand):
    return visualize_3d_model(room_layout, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand, room_type="living_room")

def visualize_3d_model(room_layout, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand, room_type):
    print("Room type: ", room_type)
    pil_image = Image.fromarray(room_layout)
    binary_data = pil_image.tobytes()
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
    if download_3d_model(
        save_path=filepath, style=style, room_type=room_type,
        objects=objects_str, room_layout=binary_data, 
        layout_width=pil_image.width, layout_height=pil_image.height
    ):
        return gr.Model3D(filepath)
    else:
        return "Failed to download 3D model."


with gr.Blocks() as demo:
    gr.Markdown('<h1 style="text-align: center;"> 3D Rooms Generator</h1>')
    with gr.Tab("Bedroom"):
        with gr.Column():
            room_type = "bedroom"
            room_layout = gr.Image()
            style = gr.Dropdown(['Light Luxury', 'Modern', 'Japanese', 
                        'Southeast Asia', 'Nordic', 'Korean', 
                        'Mediterranean', 'New Chinese', 'Vintage/Retro', 
                        'Neoclassical', 'American Country', 
                        'Ming Qing', 'Minimalist', 'Industrial', 'No style'], 
                        value="No style", 
                        label="Style")
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

    with gr.Tab("Living Room"):
        room_type = "living_room"
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Flip")

        generate_living_room_button = gr.Button("Generate Living Room")

    generate_bedroom_button.click(
        visualize_3d_bedroom, 
        inputs=[room_layout, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand], 
        outputs=output_model,
    )
    generate_living_room_button.click(
        visualize_3d_livingroom, 
        inputs=[room_layout, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand], 
        outputs=output_model,
    )

if __name__ == "__main__":
    demo.launch(share=True)