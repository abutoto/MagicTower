'''
Created on 20200107
@author abutoto
'''

import os
import sys
import pygame as pg
import pygame.freetype as ft

from conf.sysconf import *


class Form():
    def __init__(self, **kwargs):
        if "surface" in kwargs:
            self.surface = kwargs["surface"]
        elif "size" in kwargs:
            self.surface = pg.Surface(kwargs["size"])
        else:
            self.surface = None
        self.children = list()
        self.size = kwargs.get("size", (800, 600))
        self.left = kwargs.get("left", 0)
        self.top = kwargs.get("top", 0)
        self.priority = kwargs.get("priority", 0)
        ft.init()
        self.font = ft.Font(FONT_NAME, size=36)

    def set(self, surface):
        self.surface = surface
        self.rect = surface.get_rect()

    def new(self, size):
        self.surface = pg.Surface(size)
        self.rect = self.surface.get_rect()

    def add_child(self, form):
        self.children.append(form)
        self.children.sort(key=lambda x: x.priority)

    def remove_child(self, priority):
        self.children = list(
            filter(lambda x: x.priority != priority, self.children))

    def create_rect(self, p1, p2, color, size):
        pg.draw.rect(self.surface, color,
                     (p1[0], p1[1], p2[0]-p1[0], p2[1]-p1[1]), size)

    def flush(self):
        for form in self.children:
            form.flush()
            self.surface.blit(form.surface, (form.left, form.top))

    def move(self, pos):
        self.left = pos[0]
        self.top = pos[1]

    def resize(self, size):
        self.surface = pg.Surface(size)
        self.rect.w = size[0]
        self.rect.h = size[1]

    def fill(self, color):
        self.surface.fill(color)

    def fill_surface(self, surface, mode="scale", p1=(0, 0), p2=(0, 0)):
        if mode == "scale":
            self.surface.blit(pg.transform.scale(
                surface, (p2[0]-p1[0], p2[1]-p1[1])), p1)
        elif mode == "repeat":
            w, h = surface.get_rect().size
            top = p1[1]
            while top <= p2[1]:
                left = p1[0]
                while left <= p2[0]:
                    self.surface.blit(surface, (left, top))
                    left += w
                top += h
        elif mode == "norepeat":
            self.surface.blit(surface, p1)

    def fill_text(self, color, text, size=30, mode="left", fill_rect=(0, 0), width=0):
        surf, rect = self.font.render(str(text), fgcolor=color, size=size)
        rect.top = fill_rect[1]
        if mode == "left":
            rect.left = fill_rect[0]
        elif mode == "center":
            rect.left = fill_rect[0] + (width - rect.w) / 2
        elif mode == "right":
            rect.left = fill_rect[0] + width - rect.w
        else:
            rect.left = fill_rect[0]

        self.fill_surface(surf, mode="norepeat", p1=rect)
