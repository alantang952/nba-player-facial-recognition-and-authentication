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
    print(len(os.listdir(data_dir)))
    for p in os.listdir(data_dir):
        class_folder = os.path.join(data_dir, p)
        if os.path.isdir(class_folder):
            pp = os.listdir(class_folder)[0]
            file_path = os.path.join(class_folder, pp)
            if os.path.exists(file_path) and pp.endswith(ext):
                path_list.append(file_path)
    green_print('Get %d path' % len(path_list))
    return sorted(path_list)

def main():
    device = torch.device("cuda:0")
    train = my_get_paths("cropped_train", ".jpg")
    # print(train)
    mtcnn = MTCNN()
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    for t in train:
        img = Image.open(t)
        img_cropped = mtcnn(img)
        img_embedding = resnet(img_cropped.unsqueeze(0))
        #print embeddings
        print(img_embedding)




if __name__ == '__main__':
    main()
