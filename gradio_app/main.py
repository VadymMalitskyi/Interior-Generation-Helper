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


def visualize_3d_bedroom(
    room_layout,
    style,
    n_armchair,
    n_bookshelf,
    n_cabinet,
    n_ceiling_lamp,
    n_chair,
    n_children_cabinet,
    n_coffee_table,
    n_desk,
    n_double_bed,
    n_dressing_chair,
    n_dressing_table,
    n_kids_bed,
    n_nightstand,
    n_pendant_lamp,
    n_shelf,
    n_single_bed,
    n_sofa,
    n_stool,
    n_table,
    n_tv_stand,
    n_wardrobe,
):
    pil_image = Image.fromarray(room_layout)
    binary_data = pil_image.tobytes()
    print(f"Style: {style}")

    objects_dict = {
        "armchair": n_armchair,
        "bookshelf": n_bookshelf,
        "cabinet": n_cabinet,
        "ceiling_lamp": n_ceiling_lamp,
        "chair": n_chair,
        "children_cabinet": n_children_cabinet,
        "coffee_table": n_coffee_table,
        "desk": n_desk,
        "double_bed": n_double_bed,
        "dressing_chair": n_dressing_chair,
        "dressing_table": n_dressing_table,
        "kids_bed": n_kids_bed,
        "nightstand": n_nightstand,
        "pendant_lamp": n_pendant_lamp,
        "shelf": n_shelf,
        "single_bed": n_single_bed,
        "sofa": n_sofa,
        "stool": n_stool,
        "table": n_table,
        "tv_stand": n_tv_stand,
        "wardrobe": n_wardrobe,
    }
    objects_str = json.dumps(objects_dict)
    print(f"Objects: {objects_str}")

    filepath = f"created_models/{int(time.time())}.glb"
    if download_3d_model(
        save_path=filepath,
        style=style,
        room_type="bedroom",
        objects=objects_str,
        room_layout=binary_data,
        layout_width=pil_image.width,
        layout_height=pil_image.height,
    ):
        return gr.Model3D(filepath)
    else:
        return "Failed to download 3D model."


def visualize_3d_livingroom(
    room_layout,
    style,
    n_dining_chair,
    n_pendant_lamp,
    n_coffee_table,
    n_corner_side_table,
    n_dining_table,
    n_tv_stand,
    n_multi_seat_sofa,
    n_armchair,
    n_console_table,
    n_lounge_chair,
    n_stool,
    n_cabinet,
    n_bookshelf,
    n_loveseat_sofa,
    n_ceiling_lamp,
    n_wine_cabinet,
    n_l_shaped_sofa,
    n_round_end_table,
    n_shelf,
    n_chinese_chair,
    n_wardrobe,
    n_chaise_longue_sofa,
    n_desk,
    n_lazy_sofa
):
    pil_image = Image.fromarray(room_layout)
    binary_data = pil_image.tobytes()
    print(f"Style: {style}")

    objects_dict = {
        "dining_chair": n_dining_chair,
        "pendant_lamp": n_pendant_lamp,
        "coffee_table": n_coffee_table,
        "corner_side_table": n_corner_side_table,
        "dining_table": n_dining_table,
        "tv_stand": n_tv_stand,
        "multi_seat_sofa": n_multi_seat_sofa,
        "armchair": n_armchair,
        "console_table": n_console_table,
        "lounge_chair": n_lounge_chair,
        "stool": n_stool,
        "cabinet": n_cabinet,
        "bookshelf": n_bookshelf,
        "loveseat_sofa": n_loveseat_sofa,
        "ceiling_lamp": n_ceiling_lamp,
        "wine_cabinet": n_wine_cabinet,
        "l_shaped_sofa": n_l_shaped_sofa,
        "round_end_table": n_round_end_table,
        "shelf": n_shelf,
        "chinese_chair": n_chinese_chair,
        "wardrobe": n_wardrobe,
        "chaise_longue_sofa": n_chaise_longue_sofa,
        "desk": n_desk,
        "lazy_sofa": n_lazy_sofa,
    }
    objects_str = json.dumps(objects_dict)
    print(f"Objects: {objects_str}")

    filepath = f"created_models/{int(time.time())}.glb"
    if download_3d_model(
        save_path=filepath,
        style=style,
        room_type="livingroom",
        objects=objects_str,
        room_layout=binary_data,
        layout_width=pil_image.width,
        layout_height=pil_image.height,
    ):
        return gr.Model3D(filepath)
    else:
        return "Failed to download 3D model."


def visualize_3d_diningroom(
    room_layout,
    style,
    n_dining_chair,
    n_pendant_lamp,
    n_dining_table,
    n_coffee_table,
    n_corner_side_table,
    n_tv_stand,
    n_console_table,
    n_multi_seat_sofa,
    n_armchair,
    n_lounge_chair,
    n_cabinet,
    n_stool,
    n_bookshelf,
    n_ceiling_lamp,
    n_wine_cabinet,
    n_loveseat_sofa,
    n_l_shaped_sofa,
    n_shelf,
    n_round_end_table,
    n_chinese_chair,
    n_wardrobe,
    n_desk,
    n_chaise_longue_sofa,
    n_lazy_sofa
):
    pil_image = Image.fromarray(room_layout)
    binary_data = pil_image.tobytes()
    print(f"Style: {style}")

    objects_dict = {
        "dining_chair": n_dining_chair,
        "pendant_lamp": n_pendant_lamp,
        "dining_table": n_dining_table,
        "coffee_table": n_coffee_table,
        "corner_side_table": n_corner_side_table,
        "tv_stand": n_tv_stand,
        "console_table": n_console_table,
        "multi_seat_sofa": n_multi_seat_sofa,
        "armchair": n_armchair,
        "lounge_chair": n_lounge_chair,
        "cabinet": n_cabinet,
        "stool": n_stool,
        "bookshelf": n_bookshelf,
        "ceiling_lamp": n_ceiling_lamp,
        "wine_cabinet": n_wine_cabinet,
        "loveseat_sofa": n_loveseat_sofa,
        "l_shaped_sofa": n_l_shaped_sofa,
        "shelf": n_shelf,
        "round_end_table": n_round_end_table,
        "chinese_chair": n_chinese_chair,
        "wardrobe": n_wardrobe,
        "desk": n_desk,
        "chaise_longue_sofa": n_chaise_longue_sofa,
        "lazy_sofa": n_lazy_sofa,
    }
    objects_str = json.dumps(objects_dict)
    print(f"Objects: {objects_str}")

    filepath = f"created_models/{int(time.time())}.glb"
    if download_3d_model(
        save_path=filepath,
        style=style,
        room_type="diningroom",
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
            with gr.Accordion("Set objects"):
                n_armchair_bedroom = gr.Slider(-1, 5, step=1, label="armchair")
                n_bookshelf_bedroom = gr.Slider(-1, 5, step=1, label="bookshelf")
                n_cabinet_bedroom = gr.Slider(-1, 5, step=1, label="cabinet")
                n_ceiling_lamp_bedroom = gr.Slider(-1, 5, step=1, label="ceiling_lamp")
                n_chair_bedroom = gr.Slider(-1, 5, step=1, label="chair")
                n_children_cabinet_bedroom = gr.Slider(-1, 5, step=1, label="children_cabinet")
                n_coffee_table_bedroom = gr.Slider(-1, 5, step=1, label="coffee_table")
                n_desk_bedroom = gr.Slider(-1, 5, step=1, label="desk")
                n_double_bed_bedroom = gr.Slider(-1, 5, step=1, label="double_bed")
                n_dressing_chair_bedroom = gr.Slider(-1, 5, step=1, label="dressing_chair")
                n_dressing_table_bedroom = gr.Slider(-1, 5, step=1, label="dressing_table")
                n_kids_bed_bedroom = gr.Slider(-1, 5, step=1, label="kids_bed")
                n_nightstand_bedroom = gr.Slider(-1, 5, step=1, label="nightstand")
                n_pendant_lamp_bedroom = gr.Slider(-1, 5, step=1, label="pendant_lamp")
                n_shelf_bedroom = gr.Slider(-1, 5, step=1, label="shelf")
                n_single_bed_bedroom = gr.Slider(-1, 5, step=1, label="single_bed")
                n_sofa_bedroom = gr.Slider(-1, 5, step=1, label="sofa")
                n_stool_bedroom = gr.Slider(-1, 5, step=1, label="stool")
                n_table_bedroom = gr.Slider(-1, 5, step=1, label="table")
                n_tv_stand_bedroom = gr.Slider(-1, 5, step=1, label="tv_stand")
                n_wardrobe_bedroom = gr.Slider(-1, 5, step=1, label="wardrobe")
        with gr.Column():
            output_model_bedroom = gr.Model3D()

        generate_bedroom_button = gr.Button("Generate Bedroom")

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
            with gr.Accordion("Set objects"):
                n_dining_chair_livingroom = gr.Slider(-1, 5, step=1, label="dining_chair")
                n_pendant_lamp_livingroom = gr.Slider(-1, 5, step=1, label="pendant_lamp")
                n_coffee_table_livingroom = gr.Slider(-1, 5, step=1, label="coffee_table")
                n_corner_side_table_livingroom = gr.Slider(-1, 5, step=1, label="corner_side_table")
                n_dining_table_livingroom = gr.Slider(-1, 5, step=1, label="dining_table")
                n_tv_stand_livingroom = gr.Slider(-1, 5, step=1, label="tv_stand")
                n_multi_seat_sofa_livingroom = gr.Slider(-1, 5, step=1, label="multi_seat_sofa")
                n_armchair_livingroom = gr.Slider(-1, 5, step=1, label="armchair")
                n_console_table_livingroom = gr.Slider(-1, 5, step=1, label="console_table")
                n_lounge_chair_livingroom = gr.Slider(-1, 5, step=1, label="lounge_chair")
                n_stool_livingroom = gr.Slider(-1, 5, step=1, label="stool")
                n_cabinet_livingroom = gr.Slider(-1, 5, step=1, label="cabinet")
                n_bookshelf_livingroom = gr.Slider(-1, 5, step=1, label="bookshelf")
                n_loveseat_sofa_livingroom = gr.Slider(-1, 5, step=1, label="loveseat_sofa")
                n_ceiling_lamp_livingroom = gr.Slider(-1, 5, step=1, label="ceiling_lamp")
                n_wine_cabinet_livingroom = gr.Slider(-1, 5, step=1, label="wine_cabinet")
                n_l_shaped_sofa_livingroom = gr.Slider(-1, 5, step=1, label="l_shaped_sofa")
                n_round_end_table_livingroom = gr.Slider(-1, 5, step=1, label="round_end_table")
                n_shelf_livingroom = gr.Slider(-1, 5, step=1, label="shelf")
                n_chinese_chair_livingroom = gr.Slider(-1, 5, step=1, label="chinese_chair")
                n_wardrobe_livingroom = gr.Slider(-1, 5, step=1, label="wardrobe")
                n_chaise_longue_sofa_livingroom = gr.Slider(-1, 5, step=1, label="chaise_longue_sofa")
                n_desk_livingroom = gr.Slider(-1, 5, step=1, label="desk")
                n_lazy_sofa_livingroom = gr.Slider(-1, 5, step=1, label="lazy_sofa")
        with gr.Column():
            output_model_livingroom = gr.Model3D()

        generate_livingroom_button = gr.Button("Generate Living Room")
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
            with gr.Accordion("Set objects"):
                n_dining_chair_diningroom = gr.Slider(-1, 5, step=1, label="dining_chair")
                n_pendant_lamp_diningroom = gr.Slider(-1, 5, step=1, label="pendant_lamp")
                n_dining_table_diningroom = gr.Slider(-1, 5, step=1, label="dining_table")
                n_coffee_table_diningroom = gr.Slider(-1, 5, step=1, label="coffee_table")
                n_corner_side_table_diningroom = gr.Slider(-1, 5, step=1, label="corner_side_table")
                n_tv_stand_diningroom = gr.Slider(-1, 5, step=1, label="tv_stand")
                n_console_table_diningroom = gr.Slider(-1, 5, step=1, label="console_table")
                n_multi_seat_sofa_diningroom = gr.Slider(-1, 5, step=1, label="multi_seat_sofa")
                n_armchair_diningroom = gr.Slider(-1, 5, step=1, label="armchair")
                n_lounge_chair_diningroom = gr.Slider(-1, 5, step=1, label="lounge_chair")
                n_cabinet_diningroom = gr.Slider(-1, 5, step=1, label="cabinet")
                n_stool_diningroom = gr.Slider(-1, 5, step=1, label="stool")
                n_bookshelf_diningroom = gr.Slider(-1, 5, step=1, label="bookshelf")
                n_ceiling_lamp_diningroom = gr.Slider(-1, 5, step=1, label="ceiling_lamp")
                n_wine_cabinet_diningroom = gr.Slider(-1, 5, step=1, label="wine_cabinet")
                n_loveseat_sofa_diningroom = gr.Slider(-1, 5, step=1, label="loveseat_sofa")
                n_l_shaped_sofa_diningroom = gr.Slider(-1, 5, step=1, label="l_shaped_sofa")
                n_shelf_diningroom = gr.Slider(-1, 5, step=1, label="shelf")
                n_round_end_table_diningroom = gr.Slider(-1, 5, step=1, label="round_end_table")
                n_chinese_chair_diningroom = gr.Slider(-1, 5, step=1, label="chinese_chair")
                n_wardrobe_diningroom = gr.Slider(-1, 5, step=1, label="wardrobe")
                n_desk_diningroom = gr.Slider(-1, 5, step=1, label="desk")
                n_chaise_longue_sofa_diningroom = gr.Slider(-1, 5, step=1, label="chaise_longue_sofa")
                n_lazy_sofa_diningroom = gr.Slider(-1, 5, step=1, label="lazy_sofa")
        with gr.Column():
            output_model_diningroom = gr.Model3D()

        generate_diningroom_button = gr.Button("Generate Dining Room")

    generate_bedroom_button.click(
        visualize_3d_bedroom,
        inputs=[
            room_layout_bedroom,
            style_bedroom,
            n_armchair_bedroom,
            n_bookshelf_bedroom,
            n_cabinet_bedroom,
            n_ceiling_lamp_bedroom,
            n_chair_bedroom,
            n_children_cabinet_bedroom,
            n_coffee_table_bedroom,
            n_desk_bedroom,
            n_double_bed_bedroom,
            n_dressing_chair_bedroom,
            n_dressing_table_bedroom,
            n_kids_bed_bedroom,
            n_nightstand_bedroom,
            n_pendant_lamp_bedroom,
            n_shelf_bedroom,
            n_single_bed_bedroom,
            n_sofa_bedroom,
            n_stool_bedroom,
            n_table_bedroom,
            n_tv_stand_bedroom,
            n_wardrobe_bedroom,
        ],
        outputs=output_model_bedroom,
    )
    generate_livingroom_button.click(
        visualize_3d_livingroom,
        inputs=[
            room_layout_livingroom,
            style_livingroom,
            n_dining_chair_livingroom,
            n_pendant_lamp_livingroom,
            n_coffee_table_livingroom,
            n_corner_side_table_livingroom,
            n_dining_table_livingroom,
            n_tv_stand_livingroom,
            n_multi_seat_sofa_livingroom,
            n_armchair_livingroom,
            n_console_table_livingroom,
            n_lounge_chair_livingroom,
            n_stool_livingroom,
            n_cabinet_livingroom,
            n_bookshelf_livingroom,
            n_loveseat_sofa_livingroom,
            n_ceiling_lamp_livingroom,
            n_wine_cabinet_livingroom,
            n_l_shaped_sofa_livingroom,
            n_round_end_table_livingroom,
            n_shelf_livingroom,
            n_chinese_chair_livingroom,
            n_wardrobe_livingroom,
            n_chaise_longue_sofa_livingroom,
            n_desk_livingroom,
            n_lazy_sofa_livingroom,
        ],
        outputs=output_model_livingroom,
    )
    generate_diningroom_button.click(
        visualize_3d_diningroom,
        inputs=[
            room_layout_diningroom,
            style_diningroom,
            n_dining_chair_diningroom,
            n_pendant_lamp_diningroom,
            n_dining_table_diningroom,
            n_coffee_table_diningroom,
            n_corner_side_table_diningroom,
            n_tv_stand_diningroom,
            n_console_table_diningroom,
            n_multi_seat_sofa_diningroom,
            n_armchair_diningroom,
            n_lounge_chair_diningroom,
            n_cabinet_diningroom,
            n_stool_diningroom,
            n_bookshelf_diningroom,
            n_ceiling_lamp_diningroom,
            n_wine_cabinet_diningroom,
            n_loveseat_sofa_diningroom,
            n_l_shaped_sofa_diningroom,
            n_shelf_diningroom,
            n_round_end_table_diningroom,
            n_chinese_chair_diningroom,
            n_wardrobe_diningroom,
            n_desk_diningroom,
            n_chaise_longue_sofa_diningroom,
            n_lazy_sofa_diningroom,
        ],
        outputs=output_model_diningroom,
    )


if __name__ == "__main__":
    demo.launch(share=True)
