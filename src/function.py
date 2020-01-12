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

    def update_screen(self):
        self.pull()
        if global_dict["menu"] and global_dict["menu"].activate == False:
            global_dict["menu"].open()
            global_dict["rootscreen"].add_child(global_dict["menu"])

        image_group = global_dict.get("image_group")
        image_dict = global_dict.get("image_dict")[image_group]
        global_dict["map"].draw_map(image_dict)

        global_dict["map"].map_dict[global_dict["map"].floor][self.player.x][self.player.y] = 0
        rect = image_dict[self.player.face + 101].get_rect()
        rect.left = self.player.y * BLOCK_SIZE
        rect.top = self.player.x*BLOCK_SIZE
        global_dict["map"].fill_surface(image_dict[self.player.face+101],
                                        mode="norepeat", p1=(self.player.y * BLOCK_SIZE, self.player.x*BLOCK_SIZE))

    def draw_statusbar(self):
        self.pull()
        ft.init()
        font = ft.Font(FONT_NAME, size=50)
        pos_list, ftsize_list, text_list = self.player.get_status()
        for i in range(len(pos_list)):
            global_dict["rootscreen"].fill_text(
                FONT_COLOR, text_list[i], size=ftsize_list[i], mode="right", fill_rect=pos_list[i])

        floor_info = "第 {} 层".format(self.map.floor) if self.map.floor > 0 else "序 章"
        global_dict["rootscreen"].fill_text(
            FONT_COLOR, floor_info, size=25, mode="center", fill_rect=(90, 465), width=80)

        global_dict["rootscreen"].fill_text(
            FONT_COLOR, "S 保存", size=16, mode="center", fill_rect=(45, 525), width=70)
        global_dict["rootscreen"].fill_text(
            FONT_COLOR, "Q 退出程序", size=16, mode="center", fill_rect=(130, 525), width=80)
        global_dict["rootscreen"].fill_text(
            FONT_COLOR, "A 读取", size=16, mode="center", fill_rect=(45, 555), width=70)
        global_dict["rootscreen"].fill_text(
            FONT_COLOR, "R 重新开始", size=16, mode="center", fill_rect=(130, 555), width=80)

        self.push()

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
            if self.player.has_prop(215) == False:
                monster_info = Monster_Info()
                global_dict["menu"] = monster_info
        elif event.key == pg.K_j:
            if self.player.has_prop(214) == False:
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
            status = self.player.try_fight(
                global_dict["monster_dict"][move_id-300])
            if status:
                self.map.change_cell(0, pos)

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
        elif prop_id == 214:  # 楼层跳跃
            pass
        elif prop_id == 215:  # 罗盘
            pass
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

        self.player.get_prop(prop_id)

    def meet(self, npc_id):
        if npc_id == 105:  # 序章中的仙子
            self.player.yellow += 1
            self.map.change_cell(0, (8, 5))
            self.map.change_cell(npc_id, (8, 4))  # 仙子左移
            self.player.yellow = 1  # 黄钥匙+1
        elif npc_id >= 110 and npc_id <= 112:  # 商店
            shop_image = global_dict.get("image_dict")[0][111]
            info_list = ["增加 {} 点生命", "增加 {} 点攻击", "增加 {} 点防御", "离开商店"]
            goods_type = ["hp", "attack", "defense"]
            goods_addition = [800, 4, 4, ""]
            cost_type = "gold"
            cost = (25, 25, 25, 0)
            if self.map.floor == 11:
                goods_addition = [5000, 20, 20, ""]
                cost = (100, 100, 100, 0)
            title = "  想要增加你的能力吗？\n如果你有 {} 金币，你\n可以任意选择一项：".format(cost[0])
            shop = Shop(shop_image=shop_image, title=title, goods_type=goods_type,
                        goods_addition=goods_addition, info_list=info_list, cost_type=cost_type, cost=cost)
            global_dict["menu"] = shop
        elif npc_id == 107:  # 经验老人
            shop_image = global_dict.get("image_dict")[0][107]
            info_list = ["提升 {} 级（需要 {} 点）",
                         "增加攻击 {}（需要 {} 点）", "增加防御 {}（需要 {} 点）", "离开商店"]
            goods_type = ["grade", "attack", "defense"]
            goods_addition = [1, 5, 5, ""]
            cost_type = "experience"
            cost = (100, 30, 30, 0)
            if self.map.floor == 13:
                experience = [3, 20, 20, ""]
                cost = (100, 30, 30, 0)
            title = "  你好，英雄的人类，只\n要你有足够的经验，我就\n可以让你变的更加强大："
            shop = Shop(shop_image=shop_image, title=title, goods_type=goods_type,
                        goods_addition=goods_addition, info_list=info_list, cost_type=cost_type, cost=cost)
            global_dict["menu"] = shop
        elif npc_id == 110:  # 小偷
            pass
        elif npc_id == 111:  # 公主
            pass
