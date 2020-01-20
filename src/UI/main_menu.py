'''
Created on 20200108
@author zs
'''

import pygame as pg

from src.UI.form import Form
from src.UI.menu import Menu
from conf.sysconf import *
from src.global_var import global_dict


class MainMenu(Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.activate = True
        self.map = None
        self.player = None

    def draw(self):
        self.update_image_group()
        self.update_screen()
        self.draw_statusbar()
        self.update_message()

    def update_screen(self):
        self.pull()
        if global_dict["menu"] and global_dict["menu"].activate == False:
            global_dict["menu"].open()
            self.add_child(global_dict["menu"])

        image_group = global_dict.get("image_group")
        image_dict = global_dict.get("image_dict")[image_group]
        global_dict["map"].draw_map(image_dict)

        global_dict["map"].map_dict[global_dict["map"].floor][self.player.x][self.player.y] = 0
        rect = image_dict[self.player.face + 101].get_rect()
        rect.left = self.player.y * BLOCK_SIZE
        rect.top = self.player.x*BLOCK_SIZE
        global_dict["map"].fill_surface(image_dict[self.player.face+101],
                                        mode="norepeat", p1=(self.player.y * BLOCK_SIZE, self.player.x*BLOCK_SIZE))

        self.fill_surface(
            global_dict["bg_img"], mode="scale", p1=(0, 0), p2=self.size)
        self.create_rect(
            (254, 44), (772, 562), FRAME_COLOR, 0)
        self.draw_statusbar()

    def draw_statusbar(self):
        self.pull()
        pos_list, ftsize_list, text_list = self.player.get_status()
        for i in range(len(pos_list)):
            self.fill_text(
                FONT_COLOR, text_list[i], size=ftsize_list[i], mode="center", fill_rect=pos_list[i], width=100)

        floor_info = "第 {} 层".format(
            self.map.floor) if self.map.floor > 0 else "序 章"
        self.fill_text(
            FONT_COLOR, floor_info, size=25, mode="center", fill_rect=(90, 465), width=100)

        self.fill_text(
            FONT_COLOR, "S 保存", size=16, mode="center", fill_rect=(45, 525), width=70)
        self.fill_text(
            FONT_COLOR, "Q 退出程序", size=16, mode="center", fill_rect=(130, 525), width=80)
        self.fill_text(
            FONT_COLOR, "A 读取", size=16, mode="center", fill_rect=(45, 555), width=70)
        self.fill_text(
            FONT_COLOR, "R 重新开始", size=16, mode="center", fill_rect=(130, 555), width=80)

        self.push()

    def update_image_group(self):
        # 怪物、NPC动态显示
        image_group_timer = global_dict["image_group_timer"] - 1
        if image_group_timer == 0:
            image_group_timer = IMAGE_GROUP_FPS
            global_dict["image_group"] = global_dict["image_group"] ^ 1
        global_dict["image_group_timer"] = image_group_timer

    def update_message(self):
        # 显示提示消息
        message_list = list()
        top = 200
        self.remove_child(3)
        for message in global_dict.get("message", []):
            message_form = Form(priority=3)
            message_form.new((WIDTH/2, 50))
            message_form.left = WIDTH/3
            message_form.top = top
            top += 50
            message_form.fill_surface(global_dict.get("image_dict")[
                0][0], mode="repeat", p1=(0, 0), p2=message_form.size)
            message_form.fill_text(
                FONT_COLOR, message[0], size=30, mode="center", fill_rect=(0, 10), width=WIDTH/2)
            message_form.create_rect((0,0), self.size, FRAME_COLOR, 5)
            self.add_child(message_form)

            message[1] -= 1
            if message[1] > 0:
                message_list.append(message)
        global_dict["message"] = message_list
