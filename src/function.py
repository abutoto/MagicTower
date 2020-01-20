'''
Created on 20200109
@author abutoto
'''

import os
import sys
import pygame as pg
import pygame.freetype as ft

from src.global_var import global_dict
from src.UI.menu import *
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

    def action(self, event):
        self.pull()
        menu = global_dict["menu"]
        if menu and menu.activate:
            menu.action(event)
            self.push()
            return True

        if event.key == pg.K_PAGEUP:
            self.player.x, self.player.y = self.map.move_floor(1)
            self.player.face = 1
        elif event.key == pg.K_PAGEDOWN:
            self.player.x, self.player.y = self.map.move_floor(-1)
            self.player.face = 1
        elif event.key == pg.K_UP:
            self.move(0)
        elif event.key == pg.K_DOWN:
            self.move(1)
        elif event.key == pg.K_LEFT:
            self.move(2)
        elif event.key == pg.K_RIGHT:
            self.move(3)
        elif event.key == pg.K_l:
            if self.player.has_prop(215) == True:
                monster_info = Monster_Info()
                global_dict["menu"] = monster_info
        elif event.key == pg.K_j:
            if self.player.has_prop(214) == True:
                jump_menu = Jump_Menu()
                global_dict["menu"] = jump_menu

        self.push()
        return True

    def move(self, flag):
        go = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        pos = self.player.x + go[flag][0], self.player.y + go[flag][1]

        if pos[0] < 0 or pos[0] >= BLOCK_NUM or pos[1] < 0 or pos[1] >= BLOCK_NUM:
            return

        move_id = self.map.map_dict[self.map.floor][pos[0]][pos[1]]
        status = False
        if move_id < 0:  # 不可走区域
            pass
        elif move_id == 0:  # 路
            status = True
            self.player.x = pos[0]
            self.player.y = pos[1]
            self.player.face = flag
        elif move_id < 100:  # 门
            status = self.check_door(move_id)
            if status:
                self.map.change_cell(0, pos)
        elif move_id < 200:  # npc
            self.meet(move_id)
        elif move_id < 300:  # 道具
            self.get_prop(move_id)
            self.map.change_cell(0, pos)
            status = True
        elif move_id >= 300:  # 怪物
            monster = global_dict["monster_dict"][move_id-300].copy()
            monster_image = [global_dict["image_dict"][0]
                             [move_id], global_dict["image_dict"][1][move_id]]
            if self.player.can_win(monster):
                global_dict["menu"] = Fight(
                    monster=monster, pos=pos, monster_image=monster_image)
                self.monster_action(move_id)

    def check_door(self, move_id):
        status = False
        if move_id == 1:  # 上楼
            self.player.x, self.player.y = self.map.move_floor(1)
            self.player.face = 1
            status = False
        elif move_id == 2:  # 下楼
            self.player.x, self.player.y = self.map.move_floor(-1)
            self.player.face = 1
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
        message = ""
        if prop_id == 201:  # 黄钥匙
            self.player.strengthen("yellow", 1)
            message = "获得黄钥匙，黄钥匙 +1"
        elif prop_id == 202:  # 蓝钥匙
            self.player.strengthen("blue", 1)
            message = "获得蓝钥匙，蓝钥匙 +1"
        elif prop_id == 203:  # 红钥匙
            self.player.strengthen("red", 1)
            message = "获得红钥匙，红钥匙 +1"
        elif prop_id == 204:  # 红血瓶
            self.player.strengthen("hp", 200)
            message = "获取红血瓶，血量 +200"
        elif prop_id == 205:  # 蓝血瓶
            self.player.strengthen("hp", 500)
            message = "获得蓝血瓶，血量 +500"
        elif prop_id == 206:  # 蓝宝石
            self.player.strengthen("defense", 2)
            message = "获得蓝宝石，防御力 +2"
        elif prop_id == 207:  # 红宝石
            self.player.strengthen("attack", 3)
            message = "获得红宝石，攻击力 +3"
        elif prop_id == 208:  # 铁剑
            self.player.strengthen("attack", 10)
            message = "获得铁剑，攻击力 +10"
        elif prop_id == 209:  # 钢剑
            self.player.strengthen("attack", 30)
            message = "获得钢剑，攻击力 +30"
        elif prop_id == 210:  # 圣光剑
            self.player.strengthen("attack", 120)
            message = "获得圣光剑，攻击力 +120"
        elif prop_id == 211:  # 铁盾
            self.player.strengthen("defense", 10)
            message = "获得铁盾，防御力 +10"
        elif prop_id == 212:  # 钢盾
            self.player.strengthen("defense", 30)
            message = "获得钢盾，防御力 +30"
        elif prop_id == 213:  # 星光盾
            self.player.strengthen("defense", 120)
            message = "获得星光盾，防御力 +120"
        elif prop_id == 214:  # 楼层跳跃
            message = "获得风之，按 L 实现楼层跳跃"
        elif prop_id == 215:  # 罗盘
            message = "获得罗盘，按 J 查看怪物属性"
        elif prop_id == 216:  # 星光神榔
            message = "获得星光神榔"
            global_dict[107004] = 1
        elif prop_id == 217:  # 小飞羽
            self.player.strengthen( "grade", 1)
            message = "获得小飞羽，升一级"
        elif prop_id == 218:  # 大飞羽
            self.player.strengthen("grade", 3)
            message = "获得大飞羽，升三级"
        elif prop_id == 219:  # 钥匙盒
            self.player.strengthen("yellow", 1)
            self.player.strengthen("blue", 1)
            self.player.strengthen("red", 1)
            message = "获得钥匙盒，各钥匙数 +1"
        elif prop_id == 220:  # 十字架
            global_dict[105000] = 1
            message = "获得十字架"
        elif prop_id == 221:  # 金币
            self.player.strengthen("gold", 300)
            message = "获得大金币，金币 +300"
        elif prop_id == 222:  # 圣水瓶
            self.player.strengthen("hp", self.player.hp)
            message = "获得圣水瓶，血量翻倍"
        elif prop_id == 223:  # 炎之灵杖
            message = "获得炎之灵杖"
        elif prop_id == 224:  # 心之灵杖
            message = "获得心之灵杖"

        self.player.get_prop(prop_id)
        global_dict.get("message", []).append([message, 15])

    def meet(self, npc_id):
        def is_shop():
            if npc_id == 111:  # 商店
                return True
            elif npc_id == 107 and self.map.floor in (5, 13):  # 经验商店
                return True
            elif npc_id == 108 and self.map.floor in (5, 18):  # 钥匙商店
                return True
            return False

        if npc_id >= 110 and npc_id <= 112:
            npc_id = 111
        npc_dialoague = npc_id * 1000 + self.map.floor

        if is_shop():
            mune = Shop(npc_dialoague)
        else:
            if global_dict.get(npc_dialoague, 0) != -1:
                mune = Dialogue(npc_dialoague)
            else:
                mune = None

        global_dict["menu"] = mune

    def monster_action(self, monster_id):
        if monster_id == 313: # 红衣魔王
            if self.map.floor == 16: # 16层
                pass
        elif monster_id == 310: # 白衣武士
            if self.map.floor == 7:
                pass
        elif monster_id == 319: # 冥灵魔王
            if self.map.floor == 19: # 19 层
                pass
            elif self.map.floor == 21: # 21 层
                pass
