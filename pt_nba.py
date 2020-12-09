import argparse
import os
import sys

import math
import torch
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image


resnet = InceptionResnetV1().eval()
mtcnn = MTCNN()

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


def load_data(image_paths):
    nrof_samples = len(image_paths)
    images = torch.zeros(nrof_samples, 512)
    for i in range(nrof_samples):
        img = Image.open(image_paths[i])
        print(image_paths[i])
        img_cropped = mtcnn(img)
        resize_img = resnet.forward(img_cropped.unsqueeze(0))
        # print(len(resize_img[0]))
        images[i, :] = resize_img
    return images

def main():
    device = torch.device("cuda:0")
    train = my_get_paths("cropped_train", ".jpg")
    # print(train)
    
    
    num_batches = int(math.ceil(1.0*len(train) / 100.0))

    # print(num_batches)
    emb_array = torch.zeros(len(train), 512)
    for i in range(num_batches):
        print(i)
        start_index = i*100
        end_index = min((i+1)*100, len(train))
        paths_batch = train[start_index:end_index]
        images = load_data(paths_batch)
        emb_array[start_index:end_index, :] = images
    
    resnet.classify = True
    print(resnet.num_classes)
    # for t in train:
    #     img = Image.open(t)
    #     img_cropped = mtcnn(img)
    #     img_embedding = resnet(img_cropped.unsqueeze(0))
    #     #print embeddings
    #     print(img_embedding)
    




if __name__ == '__main__':
    main()
