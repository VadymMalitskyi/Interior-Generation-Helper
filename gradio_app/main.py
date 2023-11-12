import gradio as gr
import os
import requests
import time

# Bedroom dataset info
# {"bounds_translations": [-2.762500499999998, 0.045, -2.7527500000000007, 2.778441746198965, 3.6248395981292725, 2.818542771063899], 
#  "bounds_sizes": [0.0399828836528625, 0.020000020334800084, 0.012771999999999964, 2.8682, 1.7700649999999998, 1.698315], 
#  "bounds_angles": [-3.141592653589793, 3.141592653589793], 
#  "class_labels": ["armchair", "bookshelf", "cabinet", "ceiling_lamp", "chair", "children_cabinet",
#                    "coffee_table", "desk", "double_bed", "dressing_chair", "dressing_table", "kids_bed",
#                      "nightstand", "pendant_lamp", "shelf", "single_bed", "sofa", "stool", "table",
#                        "tv_stand", "wardrobe", "start", "end"], 
# "object_types": ["armchair", "bookshelf", "cabinet", "ceiling_lamp", "chair", "children_cabinet",
#                   "coffee_table", "desk", "double_bed", "dressing_chair", "dressing_table", "kids_bed",
#                     "nightstand", "pendant_lamp", "shelf", "single_bed", "sofa", "stool", "table"
#                     , "tv_stand", "wardrobe"], 
# "class_frequencies": {"nightstand": 0.27245508982035926, "double_bed": 0.17138137518067315,
#                        "wardrobe": 0.16079909147222796, "pendant_lamp": 0.12693578360520338,
#                          "ceiling_lamp": 0.06308073508156102, "tv_stand": 0.029888498864340286,
#                            "chair": 0.022816436093330582, "single_bed": 0.021216188313029113,
#                              "dressing_table": 0.020854842040057817, "cabinet": 0.020183770390253975,
#                                "table": 0.019667561428866404, "desk": 0.016260582283708445,
#                                  "stool": 0.011459838942804047, "shelf": 0.0081561015899236,
#                                    "kids_bed": 0.0081561015899236, "bookshelf": 0.0071753045632872185,
#                                      "children_cabinet": 0.0071753045632872185, "dressing_chair": 0.006142886640512079,
#                                        "armchair": 0.003716704521990502, "sofa": 0.0014970059880239522,
#                                          "coffee_table": 0.0009807970266363824}, 
# "class_order": {"nightstand": 0, "double_bed": 1, "wardrobe": 2, "pendant_lamp": 3, "ceiling_lamp": 4,
#                  "tv_stand": 5, "chair": 6, "single_bed": 7, "dressing_table": 8, "cabinet": 9, "table": 10,
#                    "desk": 11, "stool": 12, "shelf": 13, "kids_bed": 14, "bookshelf": 15, "children_cabinet": 16,
#                      "dressing_chair": 17, "armchair": 18, "sofa": 19, "coffee_table": 20}, 
# "count_furniture": {"nightstand": 5278, "double_bed": 3320, "wardrobe": 3115, "pendant_lamp": 2459,
#                      "ceiling_lamp": 1222, "tv_stand": 579, "chair": 442, "single_bed": 411, "dressing_table": 404,
#                        "cabinet": 391, "table": 381, "desk": 315, "stool": 222, "shelf": 158, "kids_bed": 158,
#                          "bookshelf": 139, "children_cabinet": 139, "dressing_chair": 119, "armchair": 72,
#                            "sofa": 29, "coffee_table": 19}
#    }

# Function to download and save the 3D model
def download_3d_model(save_path):
    response = requests.get("http://127.0.0.1:8000/generate_room")
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

# Gradio interface function
def visualize_3d_model(text):
    filepath = f"created_models/{int(time.time())}.glb"
    if download_3d_model(save_path=filepath):
        return gr.Model3D(filepath)
    else:
        return "Failed to download 3D model."


demo = gr.Interface(
    fn=visualize_3d_model,
    inputs=gr.Textbox(label="3D Model URL"),
    outputs=gr.Model3D(),
    title="3D Model Visualizer",
    description="Enter the URL of a 3D model to visualize.",
)

if __name__ == "__main__":
    demo.launch()