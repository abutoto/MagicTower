'''
Created on 20200108
@author abutoto
'''

import os
import sys
import pygame as pg
import pygame.freetype as ft

from src.UI.form import Form
from conf.sysconf import *
from src.loader import read_map


class Map(Form):
    def __init__(self, **kwargs):
        Form.__init__(self, **kwargs)
        self.set(pg.Surface((BLOCK_NUM*BLOCK_SIZE, BLOCK_NUM*BLOCK_SIZE)))
        self.left = MAP_LEFT
        self.top = MAP_TOP
        self.floor = FLOOR
        self.lock = True
        self.map_dict, self.map_pos = read_map()

    def flush(self):
        return
        img_id = global_dict.get("MONSTER_IMG_ID")
        image_dict = global_dict.get("image_dict")[img_id]
        player = global_dict.get("player")
        self.map_dict[self.floor][player.x][player.y] = 0

        for x in range(BLOCK_NUM):
            for y in range(BLOCK_NUM):
                image_id = self.map_dict[self.floor][x][y]
                self.surface.blit(
                    image_dict[image_id], (y*BLOCK_SIZE, x*BLOCK_SIZE))

        self.surface.blit(image_dict[player.face + 101],
                          (player.y*BLOCK_SIZE, player.x*BLOCK_SIZE))

    def draw_map(self, image_dict):
        #self.set(pg.Surface((BLOCK_NUM*BLOCK_SIZE, BLOCK_NUM*BLOCK_SIZE)))
        for x in range(BLOCK_NUM):
            for y in range(BLOCK_NUM):
                image_id = self.map_dict[self.floor][x][y]
                self.surface.blit(
                    image_dict[image_id], (y*BLOCK_SIZE, x*BLOCK_SIZE))

    def action(self, event):
        if self.lock == False:
            return False

        if event.key == pg.K_PAGEUP:
            self.move_floor(1)
        elif event.key == pg.K_PAGEDOWN:
            self.move_floor(-1)
        elif event.key == pg.K_UP:
            self.move(0)
        elif event.key == pg.K_DOWN:
            self.move(1)
        elif event.key == pg.K_LEFT:
            self.move(2)
        elif event.key == pg.K_RIGHT:
            self.move(3)

        return True

    def move_floor(self, floor, jump=False):
        player = global_dict.get("player")
        if not jump:
            if self.floor + floor not in self.map_dict:
                return
            self.floor += floor
            player.x, player.y = self.map_pos[self.floor][:
                                                          2] if floor > 0 else self.map_pos[self.floor][2:]
        else:
            player.x, player.y = self.map_pos[self.floor][:
                                                          2] if floor <= self.floor else self.map_pos[self.floor][2:]
            self.floor = floor
        player.face = 1

        global_dict["player"] = player

    def change_cell(self, id, pos=None):
        player = global_dict.get("player")
        if pos:
            if pos[0] < 0 or pos[0] >= BLOCK_NUM or pos[1] < 0 or pos[1] >= BLOCK_NUM:
                return
            self.map_dict[self.floor][pos[0]][pos[1]] = id
        else:
            self.map_dict[self.floor][player.x][player.y] = id

    def move(self, flag):
        player = global_dict.get("player")
        go = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        move_to = player.x + go[flag][0], player.y + go[flag][1]
        player.face = flag
        if self.check_move(move_to):
            player.x = move_to[0]
            player.y = move_to[1]

        global_dict["player"] = player

    def check_move(self, pos):
        if pos[0] < 0 or pos[0] >= BLOCK_NUM or pos[1] < 0 or pos[1] >= BLOCK_NUM:
            return False

        move_id = self.map_dict[self.floor][pos[0]][pos[1]]
        status = False
        if move_id < 0:  # 不可走区域
            pass
        elif move_id == 0:  # 路
            status = True
        elif move_id < 100:  # 门
            status = self.check_door(move_id)
        elif move_id < 200:  # npc
            pass
        elif move_id < 300:  # 道具
            pass
        elif move_id >= 300:  # 怪物
            player = global_dict.get("player")
            status = player.try_fight(global_dict["monster_dict"][move_id-300])
            global_dict["player"] = player

        return status

    def check_door(self, move_id):
        player = global_dict.get("player")
        status = False
        if move_id == 1:  # 上楼
            self.move_floor(1)
            status = False
        elif move_id == 2:  # 下楼
            self.move_floor(-1)
            status = False
        elif move_id == 3:  # 黄门
            if player.yellow > 0:
                player.yellow -= 1
                status = True
        elif move_id == 4:  # 蓝门
            if player.blue > 0:
                player.blue -= 1
                status = True
        elif move_id == 5:  # 红门
            if player.red > 0:
                player.red -= 1
                status = True
        elif move_id == 6:  # 二层门
            if self.prop.have_prop(216):
                status = True
        elif move_id == 7:  # 不可开护栏门
            pass
        elif move_id == 8:  # 可开护栏门
            status = True
        return status
