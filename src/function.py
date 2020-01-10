'''
Created on 20200109
@author abutoto
'''

import os
import sys
import pygame as pg
import pygame.freetype as ft

from src.global_var import global_dict

from conf.sysconf import *


class Function():
    def __init__(self):
        super().__init__()
        self.map = None
        self.player = None

    def pull(self):
        self.map = global_dict["map"]
        self.player = global_dict["player"]

    def push(self):
        global_dict["map"] = self.map
        global_dict["player"] = self.player

    def update_screen(self):
        self.pull()
        image_group = global_dict.get("image_group")
        image_dict = global_dict.get("image_dict")[image_group]
        global_dict["map"].draw_map(image_dict)

        global_dict["map"].map_dict[global_dict["map"].floor][self.player.x][self.player.y] = 0
        rect = image_dict[self.player.face + 101].get_rect()
        rect.left = self.player.y * BLOCK_SIZE
        rect.top = self.player.x*BLOCK_SIZE
        global_dict["map"].fill_surface(image_dict[self.player.face+101],
                                        mode="norepeat", fill_rect=rect)

    def draw_statusbar(self):
        self.pull()
        ft.init()
        font = ft.Font(FONT_NAME, size=36)
        pos_list, ftsize_list, text_list = self.player.get_status()
        for i in range(len(pos_list)):
            global_dict["rootscreen"].fill_text(
                font, FONT_COLOR, text_list[i], size=ftsize_list[i], fill_rect=pos_list[i])

        global_dict["rootscreen"].fill_text(
            font, FONT_COLOR, self.map.floor, size=25, fill_rect=(122, 467))

        self.push()

    def action(self, event):
        self.pull()

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

        self.push()
        return True

    def move_floor(self, floor, jump=False):
        if not jump:
            if self.map.floor + floor not in self.map.map_dict:
                return
            self.map.floor += floor
            self.player.x, self.player.y = self.map.map_pos[self.map.floor][:
                                                                            2] if floor > 0 else self.map.map_pos[self.map.floor][2:]
        else:
            self.player.x, self.player.y = self.map.map_pos[self.map.floor][:
                                                                            2] if floor <= self.map.floor else self.map.map_pos[self.map.floor][2:]
            self.map.floor = floor
        self.player.face = 1

    def change_cell(self, id, pos=None):
        if pos:
            if pos[0] < 0 or pos[0] >= BLOCK_NUM or pos[1] < 0 or pos[1] >= BLOCK_NUM:
                return
            self.map.map_dict[self.map.floor][pos[0]][pos[1]] = id
        else:
            self.map.map_dict[self.map.floor][self.player.x][self.player.y] = id

    def move(self, flag):
        go = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        move_to = self.player.x + go[flag][0], self.player.y + go[flag][1]
        self.player.face = flag
        if self.check_move(move_to):
            self.player.x = move_to[0]
            self.player.y = move_to[1]

    def check_move(self, pos):
        if pos[0] < 0 or pos[0] >= BLOCK_NUM or pos[1] < 0 or pos[1] >= BLOCK_NUM:
            return False

        move_id = self.map.map_dict[self.map.floor][pos[0]][pos[1]]
        status = False
        if move_id < 0:  # 不可走区域
            pass
        elif move_id == 0:  # 路
            status = True
        elif move_id < 100:  # 门
            status = self.check_door(move_id)
        elif move_id < 200:  # npc
            self.meet(move_id)
        elif move_id < 300:  # 道具
            self.get_prop(move_id)
            status = True
        elif move_id >= 300:  # 怪物
            status = self.player.try_fight(
                global_dict["monster_dict"][move_id-300])

        return status

    def check_door(self, move_id):
        status = False
        if move_id == 1:  # 上楼
            self.move_floor(1)
            status = False
        elif move_id == 2:  # 下楼
            self.move_floor(-1)
            status = False
        elif move_id == 3:  # 黄门
            if self.player.yellow > 0:
                self.player.yellow -= 1
                status = True
        elif move_id == 4:  # 蓝门
            if self.player.blue > 0:
                self.player.blue -= 1
                status = True
        elif move_id == 5:  # 红门
            if self.player.red > 0:
                self.player.red -= 1
                status = True
        elif move_id == 6:  # 二层门
            pass
        elif move_id == 7:  # 不可开护栏门
            pass
        elif move_id == 8:  # 可开护栏门
            status = True

        return status

    def get_prop(self, prop_id):
        if prop_id == 201:  # 黄钥匙
            self.player.yellow += 1
        elif prop_id == 202:  # 蓝钥匙
            self.player.blue += 1
        elif prop_id == 203:  # 红钥匙
            self.player.red += 1
        elif prop_id == 204:  # 红血瓶
            self.player.hp += 200
        elif prop_id == 205:  # 蓝血瓶
            self.player.hp += 500
        elif prop_id == 206:  # 蓝宝石
            self.player.defense += 2
        elif prop_id == 207:  # 红宝石
            self.player.attack += 3
        elif prop_id == 208:  # 铁剑
            self.player.attack += 10
        elif prop_id == 209:  # 钢剑
            self.player.attack += 30
        elif prop_id == 210:  # 圣光剑
            self.player.attack += 120
        elif prop_id == 211:  # 铁盾
            self.player.defense += 10
        elif prop_id == 212:  # 钢盾
            self.player.defense += 30
        elif prop_id == 213:  # 星光盾
            self.player.defense += 120
        elif prop_id == 216:  # 星光神榔
            pass
        elif prop_id == 217:  # 小飞羽
            self.player.grade += 1
            self.player.hp += 1000
            self.player.attack += 7
            self.player.defense += 7
        elif prop_id == 218:  # 大飞羽
            self.player.grade += 3
            self.player.hp += 3000
            self.player.attack += 21
            self.player.defense += 21
        elif prop_id == 219:  # 钥匙盒
            self.player.yellow += 1
            self.player.blue += 1
            self.player.red += 1
        elif prop_id == 220:  # 十字架
            pass
        elif prop_id == 221:  # 金币
            self.player.gold += 300
        elif prop_id == 222:  # 圣水瓶
            self.player.hp *= 2
        elif prop_id == 223:  # 炎之灵杖
            pass
        elif prop_id == 224:  # 心之灵杖
            pass

    def meet(self, npc_id):
        if npc_id == 105:  # 序章中的仙子
            self.player.yellow += 1
            self.change_cell(0, (8,5))
            self.change_cell(npc_id, (8,4)) # 仙子左移
            self.player.yellow = 1 # 黄钥匙+1
        elif npc_id >= 106 and npc_id <= 108:  # 商店
            pass
        elif npc_id == 109:  # 经验老人
            pass
        elif npc_id == 110:  # 小偷
            pass
        elif npc_id == 111:  # 公主
            pass

    def open(self):
        pass
