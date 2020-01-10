'''
Created on 20200107
@author abutoto
'''

import os
import sys
import pygame as pg
import pygame.freetype as ft

class Form():
    def __init__(self, **kwargs):
        self.surface = kwargs.get("surface", None)
        self.rect = self.surface.get_rect() if self.surface else None
        self.children = list()
        self.size = kwargs.get("size", (800, 600))
        self.left = kwargs.get("left", 0)
        self.top = kwargs.get("top", 0)
        self.priority = kwargs.get("priority", 0)

    def set(self, surface):
        self.surface = surface
        self.rect = surface.get_rect()

    def new(self, size):
        self.surface = pg.Surface(size)
        self.rect = self.surface.get_rect()

    def add_child(self, form):
        self.children.append(form)
        self.children.sort(key=lambda x: x.priority)

    def create_rect(self, p1, p2, color, size):
        pg.draw.rect(self.surface, color, (p1[0],p1[1],p2[0]-p1[0],p2[1]-p1[1]), size)

    def flush(self):
        for form in self.children:
            form.flush()
            self.surface.blit(form.surface, (form.left,form.top))

    def move(self, pos):
        self.left = pos[0]
        self.top = pos[1]

    def resize(self, size):
        self.surface = pg.Surface(size)
        self.rect.w = size[0]
        self.rect.h = size[1]
        
    def fill(self, color):
        self.surface.fill(color)

    def fill_surface(self, surface, mode="scale", fill_rect=None):
        rect = surface.get_rect()
        if fill_rect:
            rect.left = fill_rect.left
            rect.top = fill_rect.top
        else:
            fill_rect = self.rect
            rect.left = 0
            rect.top = 0

        if mode == "scale":
            self.surface.blit(pg.transform.scale(surface, (fill_rect.w,fill_rect.h)), rect)
        elif mode == "repeat":
            left_pos = rect.left
            while rect.bottom <= fill_rect.bottom:
                while rect.right <= fill_rect.right:
                    self.surface.blit(surface, rect)
                    rect.left += rect.w
                rect.left = left_pos
                rect.top += rect.h
        elif mode == "norepeat":
            self.surface.blit(surface, rect)

    def fill_text(self, font, color, text, size=30, fill_rect=(0,0)):
        font.render_to(self.surface, fill_rect, str(text), fgcolor=color, size=size)
        