import gradio as gr
import os
import json
import requests
import time


bedroom_objects = ["armchair", "bookshelf", "cabinet", "ceiling_lamp", "chair", "children_cabinet",
                   "coffee_table", "desk", "double_bed", "dressing_chair", "dressing_table", "kids_bed",
                   "nightstand", "pendant_lamp", "shelf", "single_bed", "sofa", "stool", "table",
                   "tv_stand", "wardrobe"]

# Function to download and save the 3D model
def download_3d_model(save_path, style, objects):
    json = {"style": style, "required_objects": objects}
    response = requests.post("http://127.0.0.1:8000/generate_room", json=json)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

# Gradio interface function
def visualize_3d_model_bedroom(style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand):
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
    if download_3d_model(save_path=filepath, style=style, objects=objects_str):
        return gr.Model3D(filepath)
    else:
        return "Failed to download 3D model."


def visualize_3d_model_living_room(style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand):
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
    if download_3d_model(save_path=filepath, style=style, objects=objects_str):
        return gr.Model3D(filepath)
    else:
        return "Failed to download 3D model."


with gr.Blocks() as demo:
    gr.Markdown('<h1 style="text-align: center;"> 3D Rooms Generator</h1>')
    with gr.Tab("Bedroom"):
        room_type = "bedroom"
        with gr.Column():
            style = gr.Dropdown(['Light Luxury', 'Modern', 'Japanese', 
                        'Southeast Asia', 'Nordic', 'Korean', 
                        'Mediterranean', 'New Chinese', 'Vintage/Retro', 
                        'Neoclassical', 'American Country', 
                        'Ming Qing', 'Minimalist', 'Industrial', 'No style'], value="No style", label="Style")
            with gr.Accordion("Set objects"):
                n_double_bed = gr.Slider(-1, 10, step=1, label="double_bed")
                n_wardrobe = gr.Slider(-1, 10, step=1, label="wardrobe")
                n_pendant_lamp = gr.Slider(-1, 10, step=1, label="pendant_lamp")
                n_ceiling_lamp = gr.Slider(-1, 10, step=1, label="ceiling_lamp")
                n_tv_stand = gr.Slider(-1, 10, step=1, label="tv_stand")
                n_nightstand = gr.Slider(-1, 10, step=1, label="nightstand")
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

    generate_bedroom_button.click(visualize_3d_model_bedroom, inputs=[style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand], outputs=output_model)
    generate_living_room_button.click(visualize_3d_model_living_room, inputs=[style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand], outputs=output_model)

if __name__ == "__main__":
    demo.launch(share=True)