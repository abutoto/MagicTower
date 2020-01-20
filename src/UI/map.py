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
        self.max_floor = FLOOR
        self.priority = 1
        self.map_dict, self.map_pos = read_map()
        self.player = None

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
        pos = (0, 0)
        if not jump:
            if self.floor + floor not in self.map_dict:
                return
            self.floor += floor
            pos = self.map_pos[self.floor][:
                                           2] if floor > 0 else self.map_pos[self.floor][2:]
        else:
            if floor > self.max_floor:
                return False
            pos = self.map_pos[floor][:
                                      2] if self.floor <= floor else self.map_pos[floor][2:]
            self.floor = floor

        self.max_floor = max(self.max_floor, self.floor)
        return pos

    def change_cell(self, id, pos, floor=None):
        if pos[0] < 0 or pos[0] >= BLOCK_NUM or pos[1] < 0 or pos[1] >= BLOCK_NUM:
            return
        if floor == None:
            floor = self.floor
        self.map_dict[floor][pos[0]][pos[1]] = id
