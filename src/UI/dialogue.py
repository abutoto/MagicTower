'''
Created on 20200108
@author zs
'''

import os
import sys
import pygame as pg
import pygame.freetype as ft

from src.UI.form import Form
from conf.sysconf import *
from src.global_var import global_dict


class Dialogue(Form):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_image = kwargs.get("bg_image", None)
        self.image = kwargs.get("image", None)
        self.priority = 2
        self.activate = False
        self.map = None
        self.player = None
        self.dialogue = kwargs.get("dialogue", "")

    def pull(self):
        self.map = global_dict["map"]
        self.player = global_dict["player"]

    def push(self):
        global_dict["map"] = self.map
        global_dict["player"] = self.player

    def action(self, event):
        self.pull()

        if event.key == pg.K_SPACE:
            self.dialogue = self.dialogue[1:]
            if len(self.dialogue) == 0:
                self.close()

        self.draw()

    def flush(self):
        self.draw()
        super().flush()

    def draw(self):
        self.pull()
        self.fill(BLACK)

        self.create_rect((0, 0), self.size, FRAME_COLOR, 5)
        self.fill_surface(self.bg_image, mode="repeat",
                          p1=(0, 0), p2=self.size)
        self.fill_surface(self.image, mode="norepeat", p1=(10, 12))

        hight = 30
        top = 10
        for t in self.dialogue[0].split("\n"):
            self.fill_text(FONT_COLOR, t, size=16,
                           mode="left", fill_rect=(60, top))
            top += 20

    def open(self):
        global_dict["activate"] = self.priority
        self.activate = True

    def close(self):
        global_dict["activate"] = 1
        global_dict["menu"] = None
        global_dict["rootscreen"].remove_child(self.priority)
        self.activate = False
