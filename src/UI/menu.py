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
from src.UI.shop_data import shop_info
from src.UI.dialogue_data import dialogue_info, npc_name
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
    def __init__(self, shop_id):
        super().__init__()
        self.size = (250, 250)
        self.new(self.size)
        self.left = 350
        self.top = 150
        self.size = (250, 250)
        self.create_rect((0, 0), self.size, FRAME_COLOR, 5)

        self.select = 0
        self.__dict__.update(shop_info[shop_id])
        self.shop_image = global_dict.get("image_dict")[0][shop_id//1000]
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


class Dialogue(Menu):
    def __init__(self, dialogue_id):
        super().__init__()
        self.size = (300, 90)
        self.new(self.size)

        self.dialogue_id = dialogue_id
        self.npc_status = global_dict.get(dialogue_id, 0)
        self.bg_image = global_dict.get("image_dict")[0][0]
        self.image = global_dict.get("image_dict")[0][dialogue_id//1000]
        self.player_image = global_dict.get("image_dict")[0][102]
        self.dialogue = dialogue_info[dialogue_id][self.npc_status]
        self.npc_name = npc_name[dialogue_id//1000]
        self.player_name = "勇士"
        self.step = 0

    def action(self, event):
        self.pull()

        if event.key == pg.K_SPACE:
            self.dialogue[0][0] = self.dialogue[0][0][self.step:]
            if len(self.dialogue[0][0]) == 0:
                self.dialogue = self.dialogue[1:]
                self.step = 0

            if len(self.dialogue) == 0:
                self.close()
                if self.dialogue_id == 105000:  # 仙子
                    if self.npc_status == 0:
                        self.player.yellow += 1
                        self.map.change_cell(0, (8, 5))
                        self.map.change_cell(105, (8, 4))  # 仙子左移
                        self.player.yellow = 1  # 黄钥匙+1
                        self.player.blue = 1  # 蓝钥匙+1
                        self.player.red = 1  # 红钥匙+1
                        self.npc_status = -1
                    # 拿到十字架
                    elif self.npc_status == 2:
                        self.player.hp *= 2
                        self.player.attack *= 2
                        self.player.defense *= 2
                        self.npc_status = -1
                elif self.dialogue_id == 107002:  # 2层 神秘老人（得到钢剑，攻击+30）
                    if self.npc_status == 0:
                        self.player.attack += 30
                        self.change_cell(0, (10, 7), 2)
                        self.npc_status = -1
                elif self.dialogue_id == 108002:  # 2层 商人（得到钢盾，防御+30）
                    if self.npc_status == 0:
                        self.player.defense += 30
                        self.change_cell(0, (10, 9), 2)
                        self.npc_status = -1
                elif self.dialogue_id == 110004:  # 4层 小偷
                    if self.npc_status == 0:
                        self.map.change_cell(0, (5, 1), floor=2)  # 打开第二层门
                        self.npc_status = -1
                    elif self.npc_status == 1:
                        self.map.change_cell(0, (8, 5), floor=18)  # 打通18层
                        self.map.change_cell(0, (9, 5), floor=18)
                        self.map.change_cell(0, (0, 5), floor=4)
                        self.npc_status = -1
                elif self.dialogue_id == 107015:  # 15层 神秘老人 500金币（得到圣光剑，攻击+120）
                    if self.npc_status == 0 and self.player.gold >= 500:
                        self.player.gold -= 500
                        self.player.attack += 120
                        self.map.change_cell(0, (3, 4), floor=15)
                        self.npc_status = -1
                elif self.dialogue_id == 108015:  # 15层 商人 500经验（得到圣光盾，防御+120）
                    if self.npc_status == 0 and self.player.experience >= 500:
                        self.player.experience -= 500
                        self.player.defense += 120
                        self.map.change_cell(0, (3, 6), floor=15)
                        self.npc_status = -1
                elif self.dialogue_id == 313016:  # 16层 魔王
                    self.npc_status = -1
                elif self.dialogue_id == 111018:  # 18层 公主
                    self.npc_status = -1
                elif self.dialogue_id == 313016:  # 19层 冥灵魔王
                    self.npc_status = -1
                elif self.dialogue_id == 313016:  # 21层 冥灵魔王
                    self.npc_status = -1

                global_dict[self.npc_status] = self.npc_status

        self.draw()

    def draw(self):
        self.pull()
        if len(self.dialogue) == 0:
            self.close()
            return

        self.fill(BLACK)
        self.fill_surface(self.bg_image, mode="repeat",
                          p1=(0, 0), p2=self.size)
        self.create_rect((0, 0), self.size, FRAME_COLOR, 5)
        name = self.npc_name
        if self.dialogue[0][1] == 0:
            self.fill_surface(self.image, mode="norepeat", p1=(10, 12))
            self.move((250, 250))
        else:
            self.fill_surface(self.player_image, mode="norepeat", p1=(10, 12))
            self.move((450, 400))
            name = self.player_name

        hight = 25
        width = 235
        top = 10
        self.fill_text(FONT_COLOR, name+":", size=16,
                       mode="left", fill_rect=(60, top))
        top += hight
        index = 0
        line_cnt = 0
        while index < len(self.dialogue[0][0]):
            step = 6*3
            text = self.dialogue[0][0][index:index+step]
            if "\n" in text:
                step = text.index("\n")
                text = text[:step]
                step += len("\n")
            while self.fill_text(FONT_COLOR, text, size=16, mode="left", fill_rect=(60, top), width=width) == False:
                step -= 1
                text = self.dialogue[0][0][index:index+step]
            index += step
            top += hight
            line_cnt += 1
            if line_cnt == 2:
                break

        self.step = index


class Fight(Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = global_dict.get("image_dict")[0][0]
        self.size = (740, 300)
        self.left = 30
        self.top = 40
        self.new(self.size)

        self.pull()
        self.monster = kwargs["monster"]
        self.monster_image = kwargs["monster_image"]
        self.player_image = global_dict.get("image_dict")[0][102]
        self.pos = kwargs["pos"]
        self.time = 10
        self.group_id = 0

    def action(self, event):
        pass

    def draw(self):
        self.fill(BLACK)
        self.fill_surface(self.image, mode="repeat", p1=(0, 0), p2=self.size)
        self.create_rect((0, 0), self.size, FRAME_COLOR, 10)

        self.time -= 1
        if self.time == 0:
            self.time = 10
            self.group_id = self.group_id ^ 1

            self.monster["hp"] -= self.player.attack - self.monster["defense"]
            self.monster["hp"] = max(self.monster["hp"], 0)
            if self.monster["hp"] <= 0:
                self.map.change_cell(0, self.pos)
                self.push()
                self.close()

            self.player.hp -= self.monster["attack"] - self.player.defense

        m_pos = (15, 50)
        width = 130
        left_inner = 35
        width_inner = 60
        p_pos = (self.size[0]-width-15, 50)
        self.create_rect(
            m_pos, (m_pos[0]+width, m_pos[1]+width), FRAME_COLOR, 3)
        self.fill_surface(self.monster_image[self.group_id], mode="scale", p1=(
            m_pos[0]+left_inner, m_pos[1]+left_inner), p2=(m_pos[0]+left_inner+width_inner, m_pos[1]+left_inner+width_inner))

        self.create_rect(
            p_pos, (p_pos[0]+width, p_pos[1]+width), FRAME_COLOR, 3)
        self.fill_surface(self.player_image, mode="scale", p1=(
            p_pos[0]+left_inner, p_pos[1]+left_inner), p2=(p_pos[0]+left_inner+width_inner, p_pos[1]+left_inner+width_inner))

        text_list = ["生命值: {}".format(self.monster["hp"]),
                     "攻击力: {}".format(self.monster["attack"]),
                     "防御力: {}".format(self.monster["defense"]),
                     "{} :生命值".format(self.player.hp),
                     "{} :攻击力".format(self.player.attack),
                     "{} :防御力".format(self.player.defense)]
        width = 140
        pos_list = [(m_pos[0]+width+10, 50), (m_pos[0]+width+10, 110), (m_pos[0]+width+10, 170),
                    (p_pos[0]-width-10, 50), (p_pos[0]-width-10, 110), (p_pos[0]-width-10, 170)]
        for i, text in enumerate(text_list):
            self.fill_text(FONT_COLOR, text, size=25, mode="left" if i <
                           3 else "right", fill_rect=pos_list[i], width=width)
            left = pos_list[i][0]
            height = pos_list[i][1] + 30
            self.create_rect(
                (left, height), (left+width, height), FONT_COLOR, 1)

        self.fill_text(FONT_COLOR, "怪物", size=40, mode="center",
                       fill_rect=(m_pos[0], 200), width=width)
        self.fill_text(FONT_COLOR, "勇士", size=40, mode="center",
                       fill_rect=(p_pos[0], 200), width=width)
        self.fill_text(FONT_COLOR, "VS", size=70, mode="center", fill_rect=(
            (self.size[0]-width)/2, (self.size[1]-width)/2), width=width)
