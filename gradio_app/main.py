import json
import requests
import time

import gradio as gr
from PIL import Image


bedroom_objects = [
    "armchair",
    "bookshelf",
    "cabinet",
    "ceiling_lamp",
    "chair",
    "children_cabinet",
    "coffee_table",
    "desk",
    "double_bed",
    "dressing_chair",
    "dressing_table",
    "kids_bed",
    "nightstand",
    "pendant_lamp",
    "shelf",
    "single_bed",
    "sofa",
    "stool",
    "table",
    "tv_stand",
    "wardrobe",
]
livingroom_objects = [
    "dining_chair", 
    "pendant_lamp", 
    "coffee_table", 
    "corner_side_table", 
    "dining_table", 
    "tv_stand", 
    "multi_seat_sofa", 
    "armchair", 
    "console_table", 
    "lounge_chair", 
    "stool", 
    "cabinet", 
    "bookshelf", 
    "loveseat_sofa", 
    "ceiling_lamp", 
    "wine_cabinet", 
    "l_shaped_sofa", 
    "round_end_table", 
    "shelf", 
    "chinese_chair", 
    "wardrobe", 
    "chaise_longue_sofa", 
    "desk", 
    "lazy_sofa",
]
diningroom_objects = [
    "dining_chair", 
    "pendant_lamp", 
    "dining_table", 
    "coffee_table", 
    "corner_side_table", 
    "tv_stand", 
    "console_table", 
    "multi_seat_sofa", 
    "armchair", 
    "lounge_chair", 
    "cabinet", 
    "stool", 
    "bookshelf", 
    "ceiling_lamp", 
    "wine_cabinet", 
    "loveseat_sofa", 
    "l_shaped_sofa", 
    "shelf", 
    "round_end_table", 
    "chinese_chair", 
    "wardrobe", 
    "desk", 
    "chaise_longue_sofa", 
    "lazy_sofa",
]


def download_3d_model(
    save_path, style, room_type, objects, room_layout, layout_width, layout_height
):
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
        files={"room_layout": room_layout},
    )
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    return False

def visualize_custom_3d_bedroom(
    room_layout,
    style,
    *args,
):
    return visualize_3d_room(room_layout, style, "bedroom", *args)

def visualize_custom_3d_livingroom(
    room_layout,
    style,
    *args,
):
    return visualize_3d_room(room_layout, style, "livingroom", *args)

def visualize_custom_3d_diningroom(
    room_layout,
    style,
    *args,
):
    return visualize_3d_room(room_layout, style, "diningroom", *args)

def visualize_3d_bedroom(
    room_layout,
    style,
):
    return visualize_3d_room(room_layout, style, "bedroom", *(0 for _ in range(20)))

def visualize_3d_livingroom(
    room_layout,
    style,
):
    return visualize_3d_room(room_layout, style, "livingroom", *(0 for _ in range(23)))

def visualize_3d_diningroom(
    room_layout,
    style,
):
    return visualize_3d_room(room_layout, style, "diningroom", *(0 for _ in range(23)))

def visualize_3d_room(
    room_layout,
    style,
    room_type,
    *args,
):
    pil_image = Image.fromarray(room_layout)
    binary_data = pil_image.tobytes()
    print(f"Style: {style}")

    objects = bedroom_objects
    if room_type == "livingroom":
        objects = livingroom_objects
    elif room_type == "diningroom":
        objects = diningroom_objects

    objects_dict = {key: value for key, value in zip(objects, args)}
    objects_str = json.dumps(objects_dict)
    print(f"Objects: {objects_str}")

    filepath = f"created_models/{int(time.time())}.glb"
    if download_3d_model(
        save_path=filepath,
        style=style,
        room_type=room_type,
        objects=objects_str,
        room_layout=binary_data,
        layout_width=pil_image.width,
        layout_height=pil_image.height,
    ):
        return gr.Model3D(filepath)
    else:
        return "Failed to download 3D model."


with gr.Blocks() as demo:
    gr.Markdown('<h1 style="text-align: center;"> 3D Rooms Generator</h1>')
    with gr.Tab("Bedroom"):
        with gr.Column():
            room_layout_bedroom = gr.Image()
            style_bedroom = gr.Dropdown(
                [
                    "Light Luxury",
                    "Modern",
                    "Japanese",
                    "Southeast Asia",
                    "Nordic",
                    "Korean",
                    "Mediterranean",
                    "New Chinese",
                    "Vintage/Retro",
                    "Neoclassical",
                    "American Country",
                    "Ming Qing",
                    "Minimalist",
                    "Industrial",
                    "No style",
                ],
                value="No style",
                label="Style",
            )
            generate_bedroom_button = gr.Button("Generate Bedroom")
            with gr.Accordion("Set objects", open=False):
                armchair_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="armchair")
                bookshelf_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="bookshelf")
                cabinet_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="cabinet")
                ceiling_lamp_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="ceiling_lamp")
                chair_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="chair")
                children_cabinet_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="children_cabinet")
                coffee_table_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="coffee_table")
                desk_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="desk")
                double_bed_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="double_bed")
                dressing_chair_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="dressing_chair")
                dressing_table_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="dressing_table")
                kids_bed_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="kids_bed")
                nightstand_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="nightstand")
                pendant_lamp_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="pendant_lamp")
                shelf_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="shelf")
                single_bed_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="single_bed")
                sofa_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="sofa")
                stool_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="stool")
                table_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="table")
                tv_stand_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="tv_stand")
                wardrobe_bedroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="wardrobe")
            generate_custom_bedroom_button = gr.Button("Generate Custom Bedroom")
        with gr.Column():
            output_model_bedroom = gr.Model3D()

    with gr.Tab("Living Room"):
        with gr.Column():
            room_layout_livingroom = gr.Image()
            style_livingroom = gr.Dropdown(
                [
                    "Light Luxury",
                    "Modern",
                    "Japanese",
                    "Southeast Asia",
                    "Nordic",
                    "Korean",
                    "Mediterranean",
                    "New Chinese",
                    "Vintage/Retro",
                    "Neoclassical",
                    "American Country",
                    "Ming Qing",
                    "Minimalist",
                    "Industrial",
                    "No style",
                ],
                value="No style",
                label="Style",
            )
            generate_livingroom_button = gr.Button("Generate Living Room")
            with gr.Accordion("Set objects", open=False):
                dining_chair_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="dining_chair")
                pendant_lamp_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="pendant_lamp")
                coffee_table_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="coffee_table")
                corner_side_table_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="corner_side_table")
                dining_table_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="dining_table")
                tv_stand_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="tv_stand")
                multi_seat_sofa_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="multi_seat_sofa")
                armchair_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="armchair")
                console_table_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="console_table")
                lounge_chair_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="lounge_chair")
                stool_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="stool")
                cabinet_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="cabinet")
                bookshelf_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="bookshelf")
                loveseat_sofa_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="loveseat_sofa")
                ceiling_lamp_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="ceiling_lamp")
                wine_cabinet_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="wine_cabinet")
                l_shaped_sofa_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="l_shaped_sofa")
                round_end_table_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="round_end_table")
                shelf_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="shelf")
                chinese_chair_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="chinese_chair")
                wardrobe_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="wardrobe")
                chaise_longue_sofa_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="chaise_longue_sofa")
                desk_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="desk")
                lazy_sofa_livingroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="lazy_sofa")
            generate_custom_livingroom_button = gr.Button("Generate Custom Living Room")
        with gr.Column():
            output_model_livingroom = gr.Model3D()

    with gr.Tab("Dining Room"):
        with gr.Column():
            room_layout_diningroom = gr.Image()
            style_diningroom = gr.Dropdown(
                [
                    "Light Luxury",
                    "Modern",
                    "Japanese",
                    "Southeast Asia",
                    "Nordic",
                    "Korean",
                    "Mediterranean",
                    "New Chinese",
                    "Vintage/Retro",
                    "Neoclassical",
                    "American Country",
                    "Ming Qing",
                    "Minimalist",
                    "Industrial",
                    "No style",
                ],
                value="No style",
                label="Style",
            )
            generate_diningroom_button = gr.Button("Generate Dining Room")
            with gr.Accordion("Set objects", open=False):
                dining_chair_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="dining_chair")
                pendant_lamp_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="pendant_lamp")
                dining_table_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="dining_table")
                coffee_table_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="coffee_table")
                corner_side_table_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="corner_side_table")
                tv_stand_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="tv_stand")
                console_table_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="console_table")
                multi_seat_sofa_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="multi_seat_sofa")
                armchair_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="armchair")
                lounge_chair_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="lounge_chair")
                cabinet_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="cabinet")
                stool_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="stool")
                bookshelf_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="bookshelf")
                ceiling_lamp_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="ceiling_lamp")
                wine_cabinet_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="wine_cabinet")
                loveseat_sofa_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="loveseat_sofa")
                l_shaped_sofa_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="l_shaped_sofa")
                shelf_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="shelf")
                round_end_table_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="round_end_table")
                chinese_chair_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="chinese_chair")
                wardrobe_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="wardrobe")
                desk_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="desk")
                chaise_longue_sofa_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="chaise_longue_sofa")
                lazy_sofa_diningroom = gr.Dropdown([-1, 0, 1, 2, 3], value=-1, label="lazy_sofa")
            generate_custom_diningroom_button = gr.Button("Generate Custom Dining Room")
        with gr.Column():
            output_model_diningroom = gr.Model3D()

    generate_bedroom_button.click(
        visualize_3d_bedroom,
        inputs=[
            room_layout_bedroom,
            style_bedroom,
        ],
        outputs=output_model_bedroom,
    )
    generate_livingroom_button.click(
        visualize_3d_livingroom,
        inputs=[
            room_layout_livingroom,
            style_livingroom,
        ],
        outputs=output_model_livingroom,
    )
    generate_diningroom_button.click(
        visualize_3d_diningroom,
        inputs=[
            room_layout_diningroom,
            style_diningroom,
        ],
        outputs=output_model_diningroom,
    )
    generate_custom_bedroom_button.click(
        visualize_custom_3d_bedroom,
        inputs=[
            room_layout_bedroom,
            style_bedroom,
            armchair_bedroom,
            bookshelf_bedroom,
            cabinet_bedroom,
            ceiling_lamp_bedroom,
            chair_bedroom,
            children_cabinet_bedroom,
            coffee_table_bedroom,
            desk_bedroom,
            double_bed_bedroom,
            dressing_chair_bedroom,
            dressing_table_bedroom,
            kids_bed_bedroom,
            nightstand_bedroom,
            pendant_lamp_bedroom,
            shelf_bedroom,
            single_bed_bedroom,
            sofa_bedroom,
            stool_bedroom,
            table_bedroom,
            tv_stand_bedroom,
            wardrobe_bedroom,
        ],
        outputs=output_model_bedroom,
    )
    generate_custom_livingroom_button.click(
        visualize_custom_3d_livingroom,
        inputs=[
            room_layout_livingroom,
            style_livingroom,
            dining_chair_livingroom,
            pendant_lamp_livingroom,
            coffee_table_livingroom,
            corner_side_table_livingroom,
            dining_table_livingroom,
            tv_stand_livingroom,
            multi_seat_sofa_livingroom,
            armchair_livingroom,
            console_table_livingroom,
            lounge_chair_livingroom,
            stool_livingroom,
            cabinet_livingroom,
            bookshelf_livingroom,
            loveseat_sofa_livingroom,
            ceiling_lamp_livingroom,
            wine_cabinet_livingroom,
            l_shaped_sofa_livingroom,
            round_end_table_livingroom,
            shelf_livingroom,
            chinese_chair_livingroom,
            wardrobe_livingroom,
            chaise_longue_sofa_livingroom,
            desk_livingroom,
            lazy_sofa_livingroom,
        ],
        outputs=output_model_livingroom,
    )
    generate_custom_diningroom_button.click(
        visualize_custom_3d_diningroom,
        inputs=[
            room_layout_diningroom,
            style_diningroom,
            dining_chair_diningroom,
            pendant_lamp_diningroom,
            dining_table_diningroom,
            coffee_table_diningroom,
            corner_side_table_diningroom,
            tv_stand_diningroom,
            console_table_diningroom,
            multi_seat_sofa_diningroom,
            armchair_diningroom,
            lounge_chair_diningroom,
            cabinet_diningroom,
            stool_diningroom,
            bookshelf_diningroom,
            ceiling_lamp_diningroom,
            wine_cabinet_diningroom,
            loveseat_sofa_diningroom,
            l_shaped_sofa_diningroom,
            shelf_diningroom,
            round_end_table_diningroom,
            chinese_chair_diningroom,
            wardrobe_diningroom,
            desk_diningroom,
            chaise_longue_sofa_diningroom,
            lazy_sofa_diningroom,
        ],
        outputs=output_model_diningroom,
    )


if __name__ == "__main__":
    demo.launch(share=True)
