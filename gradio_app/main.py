import gradio as gr
import os
import json
import requests
import time


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
def visualize_3d_model(room_type, style, n_double_bed, n_wardrobe, n_pendant_lamp, n_ceiling_lamp, n_tv_stand, n_nightstand):
    print(f"Room type: {room_type}")
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


demo = gr.Interface(
    fn=visualize_3d_model,
    inputs=[
        gr.Dropdown(["bedroom", "living_room"], label="Room Type"),
        gr.Dropdown(['Light Luxury', 'Modern', 'Japanese', 
                     'Southeast Asia', 'Nordic', 'Korean', 
                     'Mediterranean', 'New Chinese', 'Vintage/Retro', 
                     'Neoclassical', 'American Country', 
                     'Ming Qing', 'Minimalist', 'Industrial', 'No style'], label="Style"),
        gr.Slider(-1, 10, step=1, label="double_bed"),
        gr.Slider(-1, 10, step=1, label="wardrobe"),
        gr.Slider(-1, 10, step=1, label="pendant_lamp"),
        gr.Slider(-1, 10, step=1, label="ceiling_lamp"),
        gr.Slider(-1, 10, step=1, label="tv_stand"),
        gr.Slider(-1, 10, step=1, label="nightstand"),
    ],
    outputs=gr.Model3D(),
    title="3D Model Visualizer",
    description="Enter the URL of a 3D model to visualize.",
)

if __name__ == "__main__":
    demo.launch()