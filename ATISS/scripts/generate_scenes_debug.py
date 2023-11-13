# 
# Copyright (C) 2021 NVIDIA Corporation.  All rights reserved.
# Licensed under the NVIDIA Source Code License.
# See LICENSE at https://github.com/nv-tlabs/ATISS.
# Authors: Despoina Paschalidou, Amlan Kar, Maria Shugrina, Karsten Kreis,
#          Andreas Geiger, Sanja Fidler
# 

"""Script used for generating scenes using a previously trained model."""
import argparse
import logging
import os
import sys
import time

import numpy as np
import torch
import trimesh

from training_utils import load_config
from utils import floor_plan_from_scene, export_scene

from scene_synthesis.datasets import filter_function, \
    get_dataset_raw_and_encoded
from scene_synthesis.datasets.threed_future_dataset import ThreedFutureDataset
from scene_synthesis.networks import build_network
from scene_synthesis.utils import get_textured_objects

from simple_3dviz import Scene
from simple_3dviz.window import show
from simple_3dviz.behaviours.keyboard import SnapshotOnKey, SortTriangles
from simple_3dviz.behaviours.misc import LightToCamera
from simple_3dviz.behaviours.movements import CameraTrajectory
from simple_3dviz.behaviours.trajectory import Circle
from simple_3dviz.behaviours.io import SaveFrames, SaveGif
from simple_3dviz.utils import render


class args:
    config_file = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/config/bedrooms_config.yaml"
    output_directory = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/visualizations"
    path_to_pickled_3d_futute_models = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/data/pickle_data/threed_future_model_bedroom.pkl"
    path_to_floor_plan_textures = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/demo/floor_plan_texture_images"
    weight_file = "/home/vadym_wsl/projects/Interior-Generation-Helper/ATISS/trained_models/L1F6VFKD0/model_01000"
    n_sequences = 1
    without_screen = True
    file_save_name = "test.glb"
    window_size = (512, 512)
    up_vector = (0., 1., 0.)
    camera_target = (0., 0., 0.)
    camera_position = (-0.10923499, 1.9325259, -7.19009)
    scene_id = None
    required_style = "Ming Qing"
    with_rotating_camera = None
    background = (1., 1., 1., 1.)
    n_frames = 1

# Disable trimesh's logger
logging.getLogger("trimesh").setLevel(logging.ERROR)

if torch.cuda.is_available():
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")
print("Running code on", device)

# Check if output directory exists and if it doesn't create it
if not os.path.exists(args.output_directory):
    os.makedirs(args.output_directory)

config = load_config(args.config_file)

raw_dataset, train_dataset = get_dataset_raw_and_encoded(
    config["data"],
    filter_fn=filter_function(
        config["data"],
        split=config["training"].get("splits", ["train", "val"])
    ),
    split=config["training"].get("splits", ["train", "val"])
)

# Build the dataset of 3D models
objects_dataset = ThreedFutureDataset.from_pickled_dataset(
    args.path_to_pickled_3d_futute_models
)
print("Loaded {} 3D-FUTURE models".format(len(objects_dataset)))

raw_dataset, dataset = get_dataset_raw_and_encoded(
    config["data"],
    filter_fn=filter_function(
        config["data"],
        split=config["validation"].get("splits", ["test"])
    ),
    split=config["validation"].get("splits", ["test"])
)
print("Loaded {} scenes with {} object types:".format(
    len(dataset), dataset.n_object_types)
)

network, _, _ = build_network(
    dataset.feature_size, dataset.n_classes,
    config, args.weight_file, device=device
)
network.eval()

# Create the scene and the behaviour list for simple-3dviz
scene = Scene(size=args.window_size)
scene.up_vector = args.up_vector
scene.camera_target = args.camera_target
scene.camera_position = args.camera_position
scene.light = args.camera_position

given_scene_id = None
if args.scene_id:
    for i, di in enumerate(raw_dataset):
        if str(di.scene_id) == args.scene_id:
            given_scene_id = i

classes = np.array(dataset.class_labels)
for i in range(args.n_sequences):
    scene_idx = given_scene_id or np.random.choice(len(dataset))
    current_scene = raw_dataset[scene_idx]
    print("{} / {}: Using the {} floor plan of scene {}".format(
        i, args.n_sequences, scene_idx, current_scene.scene_id)
    )
    # Get a floor plan
    floor_plan, tr_floor, room_mask = floor_plan_from_scene(
        current_scene, args.path_to_floor_plan_textures
    )

    bbox_params = network.generate_boxes(
        room_mask=room_mask.to(device),
        device=device
    )
    boxes = dataset.post_process(bbox_params)
    bbox_params_t = torch.cat([
        boxes["class_labels"],
        boxes["translations"],
        boxes["sizes"],
        boxes["angles"]
    ], dim=-1).cpu().numpy()

    renderables, trimesh_meshes = get_textured_objects(
        bbox_params_t, objects_dataset, classes, query_style=args.required_style
    )
    renderables += floor_plan
    trimesh_meshes += tr_floor

    if args.without_screen:
        # Do the rendering
        path_to_image = "{}/{}_{}_{:03d}".format(
            args.output_directory,
            current_scene.scene_id,
            scene_idx,
            i
        )
        behaviours = [
            LightToCamera(),
            SaveFrames(path_to_image+".png", 1)
        ]
        if args.with_rotating_camera:
            behaviours += [
                CameraTrajectory(
                    Circle(
                        [0, args.camera_position[1], 0],
                        args.camera_position,
                        args.up_vector
                    ),
                    speed=1/360
                ),
                SaveGif(path_to_image+".gif", 1)
            ]

        render(
            renderables,
            behaviours=behaviours,
            size=args.window_size,
            camera_position=args.camera_position,
            camera_target=args.camera_target,
            up_vector=args.up_vector,
            background=args.background,
            n_frames=args.n_frames,
            scene=scene
        )
    else:
        show(
            renderables,
            behaviours=[LightToCamera(), SnapshotOnKey(), SortTriangles()],
            size=args.window_size,
            camera_position=args.camera_position,
            camera_target=args.camera_target,
            up_vector=args.up_vector,
            background=args.background,
            title="Generated Scene"
        )
    if trimesh_meshes is not None:
        # Create a trimesh scene and export it
        path_to_objs = os.path.join(
            args.output_directory,
            "{:03d}_scene".format(i)
        )
        if not os.path.exists(path_to_objs):
            os.mkdir(path_to_objs)
        export_scene(path_to_objs, trimesh_meshes)
        combined = trimesh.util.concatenate(trimesh_meshes)
        # TODO: Make mesh brighter
        # has_vertex_colors = combined.visual.vertex_colors is not None
        # print("has_vertex_colors", has_vertex_colors)
        # print(combined.visual.vertex_colors.shape)
        # for i in range(len(combined.visual.vertex_colors)):
        #     combined.visual.vertex_colors[i] += 50
        # combined.visual.vertex_colors
        combined.export(
            os.path.join(
                path_to_objs,
                f"{args.output_directory}/{args.file_save_name}.glb"),
        file_type='glb')
