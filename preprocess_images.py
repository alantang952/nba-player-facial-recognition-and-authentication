import argparse
import os
import sys

import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image


def green_print(line):
    """Print in green"""
    print('\033[92m'+line+'\033[0m')

def my_get_paths(data_dir, ext):
    """Get filepath from data_dir"""
    path_list = []
    # print(os.listdir(data_dir))
    # print(len(os.listdir(data_dir)))
    for p in os.listdir(data_dir):
        class_folder = os.path.join(data_dir, p)
        if os.path.isdir(class_folder) and class_folder:
            pp = os.listdir(class_folder)
            pp = [k for k in pp if k not in '.DS_Store']
            pp = pp[0]
            # print(class_folder)
            file_path = os.path.join(class_folder, pp)
            if os.path.exists(file_path) and pp.endswith(ext):
                path_list.append(file_path)
    green_print('Get %d path' % len(path_list))
    return sorted(path_list)

def preprocess(mode):
    # device = torch.device("cuda:0")
    data_paths = my_get_paths(mode, ".jpg")
    mtcnn = MTCNN()
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    i = 0
    for d in data_paths:
        print(i)
        print(d)
        img = Image.open(d).convert("RGB")
        # print(img)
        player_name = d[d.index("/") + 1:]
        player_name = (player_name[:player_name.index("/")]).lower()
        player_name = player_name[:player_name.index(
            ",")] + "_" + player_name[player_name.index(",") + 2:]
        # print(player_name)
        save_path = "cropped_" + mode + "/" + player_name + "/" + player_name + "0001" + ".jpg"
        img_cropped = mtcnn(img, save_path)
        i += 1

def preprocess_test():
    data_paths = my_get_paths("test", ".jpg")
    print(data_paths)

# my_get_paths_train("scraped_train", ".jpg")


# preprocess("train")
preprocess("test")
# preprocess_train()
    
