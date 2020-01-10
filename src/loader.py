'''
Created on 20200101
@author zs
'''

import os
import sys
import pygame
import json

from conf.sysconf import *


def read_file(path, sp="\t"):
    with open(path, "r", encoding='utf-8') as f:
        for line in f:
            line = line.strip().split(sp)
            yield line


def read_image_dict():
    img_dict = [dict(), dict()]
    for line in read_file(FLOOR_PATH, "="):
        if len(line) != 2 or len(line[1]) == 0:
            continue
        img_id = int(line[0])
        img_path = "image/{}.png".format(line[1])
        if os.path.exists(img_path):
            img_dict[0][img_id] = load_image(img_path)
            img_dict[1][img_id] = img_dict[0][img_id]
            if "map0" in img_path:
                img_path = img_path.replace("map0", "map1")
                img_dict[1][img_id] = load_image(img_path)

    return img_dict


def load_image(path):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))
    return img


def read_map():
    floor_dict = dict()
    floor_pos = dict()
    dir_path = "conf/floor/"
    for file in os.listdir(dir_path):
        floor_id = int(file[:-4])
        file_path = dir_path + file
        floor = []
        for line in read_file(file_path, ","):
            line = [int(i) for i in line]
            if floor_id not in floor_pos:
                floor_pos[floor_id] = line
                continue

            if len(line) != BLOCK_NUM:
                print(file, floor_id, line)
                continue

            floor.append(line)

        if len(floor) != BLOCK_NUM:
            print(floor_id)
            continue

        floor_dict[floor_id] = floor

    return floor_dict, floor_pos


def read_monster():
    monster_dict = dict()
    header = []
    for line in read_file(MONSTER_PATH, ","):
        line = [i.strip() for i in line]
        if len(header) == 0:
            header = line
            continue
        line[:-1] = [int(i) for i in line[:-1]]
        line[-1] = line[-1].strip()
        line = dict(zip(header, line))
        monster_id = line["monster_id"]
        monster_dict[monster_id] = line

    return monster_dict

