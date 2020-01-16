'''
Created on 20200108
@author zs
'''

import os
import sys
import math
import pygame as pg
import pygame.freetype as ft

from src.UI.form import Form
from conf.sysconf import *
from src.global_var import global_dict


class Menu(Form):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.priority = 2
        self.activate = False
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
        self.draw()

    def flush(self):
        self.draw()
        super().flush()

    def draw(self):
        self.pull()
        self.fill(BLACK)

    def open(self):
        global_dict["activate"] = self.priority
        self.activate = True

    def close(self):
        global_dict["activate"] = 1
        global_dict["menu"] = None
        global_dict["rootscreen"].remove_child(self.priority)
        self.activate = False


class Shop(Menu):
    def __init__(self, **kwargs):
        kwargs["surface"] = pg.Surface((250, 250))
        super().__init__(**kwargs)
        self.left = 350
        self.top = 150
        self.size = (250, 250)
        self.create_rect((0, 0), self.size, FRAME_COLOR, 5)

        self.select = 0
        self.__dict__.update(kwargs)
        self.goods_num = len(self.goods_addition)
        self.shop_image_rect = self.shop_image.get_rect()
        self.key_dict = {pg.K_UP: -1, pg.K_DOWN: 1,
                         pg.K_SPACE: "buy", pg.K_ESCAPE: "close"}

    def action(self, event):
        self.pull()

        if event.key not in self.key_dict:
            return
        key_action = self.key_dict[event.key]
        if isinstance(key_action, int):
            self.select += key_action
            self.select = min(max(self.select, 0), self.goods_num-1)
        elif key_action == "buy":
            if self.select == self.goods_num - 1:
                self.close()
            else:
                buy = False
                if self.cost_type == "gold":
                    if self.player.gold >= self.cost[self.select]:
                        self.player.gold -= self.cost[self.select]
                        buy = True
                elif self.cost_type == "experience":
                    if self.player.experience >= self.cost[self.select]:
                        self.player.experience -= self.cost[self.select]
                        buy = True
                elif self.cost_type == "yellow":
                    if self.player.yellow >= self.cost[self.select]:
                        self.player.yellow -= self.cost[self.select]
                        buy = True
                elif self.cost_type == "blue":
                    if self.player.blue >= self.cost[self.select]:
                        self.player.blue -= self.cost[self.select]
                        buy = True
                elif self.cost_type == "red":
                    if self.player.red >= self.cost[self.select]:
                        self.player.red -= self.cost[self.select]
                        buy = True

                if buy:
                    self.player.strengthen(
                        self.goods_type[self.select], self.goods_addition[self.select])
        elif key_action == "close":
            self.close()

        self.draw()

    def draw(self):
        super().draw()
        self.fill(BLACK)
        self.create_rect((0, 0), self.size, FRAME_COLOR, 5)

        self.fill_surface(self.shop_image, mode="norepeat",
                          p1=(10, 12))
        hight = 35
        top = 10
        for t in self.title.split("\n"):
            self.fill_text(FONT_COLOR, t, size=16,
                           mode="left", fill_rect=(60, top))
            top += 20
        top += 25
        for i in range(self.goods_num):
            info = self.info_list[i].format(
                self.goods_addition[i], self.cost[i])
            self.fill_text(FONT_COLOR, info, size=16,
                           mode="center", fill_rect=(0, top), width=self.size[0])
            if i == self.select:
                self.create_rect((10, top-10), (240, top+30), GREEN, 3)
            top += hight


class Monster_Info(Menu):
    def __init__(self, **kwargs):
        kwargs["surface"] = pg.Surface(
            (BLOCK_NUM*BLOCK_SIZE, BLOCK_NUM*BLOCK_SIZE))
        super().__init__(**kwargs)
        self.left = MAP_LEFT
        self.top = MAP_TOP
        self.size = (BLOCK_NUM*BLOCK_SIZE, BLOCK_NUM*BLOCK_SIZE)

        self.get_monsters()

    def action(self, event):
        if event.key == pg.K_l:
            self.close()
        elif event.key == pg.K_LEFT:
            self.page -= 1
            self.page = min(max(self.page, 0), self.max_page-1)
        elif event.key == pg.K_RIGHT:
            self.page += 1
            self.page = min(max(self.page, 0), self.max_page-1)

        return True

    def draw(self):
        super().draw()

        left = 10
        top = 10
        height = 60
        self.children = list()
        pos = self.page * self.page_size
        for monster in self.monsters[pos: pos+self.page_size]:
            monster_form = self.draw_monster(monster[0], monster[1])
            monster_form.left = left
            monster_form.top = top
            top += height
            self.add_child(monster_form)

    def draw_monster(self, monster, monster_image):
        surface = Form(surface=pg.Surface(
            (BLOCK_SIZE*(BLOCK_NUM-1), 70)))
        surface.create_rect(
            (3, 3), (BLOCK_SIZE+7, BLOCK_SIZE+7), FRAME_COLOR, 5)
        surface.surface.blit(monster_image, (5, 5))

        text_list = [["名称", monster["name"], "攻击", monster["attack"], "金 - 经", "{} - {}".format(monster["gold"], monster["experience"])],
                     ["生命", monster["hp"], "防御",  monster["defense"], "损失", self.player.get_heart(monster)]]
        width_list = [40, 80, 40, 80, 70, 60]
        hight = 30
        top = 5
        width = 65
        for row in text_list:
            left = 65
            for i, text in enumerate(row):
                surface.fill_text(FONT_COLOR, text, size=16,
                                  mode="center", fill_rect=(left, top), width=width_list[i])
                left += width_list[i]
            top += hight

        return surface

    def get_monsters(self):
        self.pull()

        monster_dict = global_dict["monster_dict"]
        image_dict = global_dict.get("image_dict")[0]

        monsters = set()
        for i in range(BLOCK_NUM):
            for j in range(BLOCK_NUM):
                monster_id = self.map.map_dict[self.map.floor][i][j] - 300
                if monster_id not in monster_dict:
                    continue
                monsters.add(monster_id)

        self.monsters = list()
        for monster_id in sorted(monsters):
            monster = monster_dict[monster_id]
            monster_image = image_dict[monster_id+300]
            self.monsters.append((monster, monster_image))

        self.page = 0
        self.page_size = 8
        self.max_page = math.ceil(len(self.monsters) / self.page_size)


class Jump_Menu(Menu):
    def __init__(self, **kwargs):
        kwargs["surface"] = pg.Surface((400, 400))
        super().__init__(**kwargs)
        self.left = 270
        self.top = 100
        self.size = (400, 400)
        self.create_rect((0, 0), self.size, FRAME_COLOR, 5)

        self.x = 0
        self.y = 0
        self.draw()

    def action(self, event):
        self.pull()

        if event.key == pg.K_UP:
            self.x = self.x-1 if self.x > 0 else self.x
        elif event.key == pg.K_DOWN:
            self.x = self.x+1 if self.x < 6 else self.x
        elif event.key == pg.K_LEFT:
            self.y = self.y-1 if self.y > 0 else self.y
        elif event.key == pg.K_RIGHT:
            self.y = self.y+1 if self.y < 2 else self.y
        elif event.key == pg.K_j:
            self.close()
        elif event.key == pg.K_SPACE:
            floor = self.x * 3 + self.y + 1
            pos = self.map.move_floor(floor, True)
            if pos:
                self.player.x, self.player.y = pos
                self.player.face = 1
                self.close()

        self.draw()

    def draw(self):
        super().draw()
        self.fill(BLACK)
        self.create_rect((0, 0), self.size, FRAME_COLOR, 5)

        self.fill_text(FONT_COLOR, "楼层跳跃", size=50,
                       mode="center", fill_rect=(0, 30), width=self.size[0])

        left = 5
        top = 100
        height = 40
        width = 130
        row_num = 3
        for i in range(1, 21):
            self.fill_text(FONT_COLOR, "第 {} 层".format(i), size=18,
                           mode="center", fill_rect=(left, top), width=width)
            if i-1 == self.x * 3 + self.y:
                self.create_rect((left+5, top-10),
                                 (left+width-5, top+25), GREEN, 3)
            if i % row_num == 0:
                left = 5
                top += height
            else:
                left += width
