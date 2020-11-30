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

def main(args):
    device = torch.device("cuda:0")
    data_paths = my_get_paths(args.data_dir, args.image_ext)
    mtcnn = MTCNN()
    resnet = InceptionResnetV1(pretrained='vggface2').eval()

    #preprocess images

    i = 0
    print(len(data_paths))
    for d in data_paths:
        print(i)
        print(d)
        img = Image.open(d)
        player_name = d[d.index("/") + 1:]
        player_name = (player_name[:player_name.index("/")]).lower()
        player_name = player_name[:player_name.index(",")] + "_" + player_name[player_name.index(",") + 2: ]
        # print(player_name)
        save_path = "cropped/" + player_name + "/" + player_name + "0001" +".jpg"
        img_cropped = mtcnn(img, save_path)
        i += 1




    # img_embedding = resnet(img_cropped.unsqueeze(0))
    # print(img_embedding)
    # green_print('Model loaded')
    # embeddings
    # inputs




#copied from tensorflow implementation
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, help='model used to dump embeddings',
                        default='20170512-110547/')
    parser.add_argument('data_dir', type=str, help='images root folder')
    parser.add_argument('--register_order_file', type=str, help='the register order file',
                        default='auto-gen')

    parser.add_argument('--csv_filename', type=str,
                        help='filename of output csv file')
    parser.add_argument('--batch_size', type=int, default=100)
    parser.add_argument('--image_size', type=int, default=160)
    parser.add_argument('--image_ext', type=str, default='jpg')

    parser.add_argument('--gpu_memory_fraction', type=float, default=0.8)
    parser.add_argument('--gpu', type=int, default=0)

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
