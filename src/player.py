'''
Created on 20200101
@author abutoto
'''

import os
import sys
import pygame
import pygame.freetype
import math

from conf.sysconf import *
from src.global_var import *


class Player():
    def __init__(self):
        self.x = PLAY_X
        self.y = PLAY_Y
        self.face = PLAY_FACE
        self.grade = PLAY_GRADE
        self.hp = PLAY_HP
        self.attack = PLAY_ATTACK
        self.defense = PLAY_DEFENSE
        self.gold = PLAY_GOLD
        self.experience = PLAY_EXPERIENCE
        self.yellow = PLAY_YELLOW
        self.blue = PLAY_BLUE
        self.red = PLAY_RED

        print("Player")

    def try_fight(self, monster):
        h1 = self.attack - monster["defense"]
        h2 = monster["attack"] - self.defense
        if h1 <= 0:
            return False
        round = math.ceil((monster["hp"] - h1) / h1)
        if round * h2 >= self.hp:
            return False
        self.hp -= round * h2
        self.experience += monster["experience"]
        self.gold += monster["gold"]
        return True

    def get_status(self):
        pos_list = [(150, 70), (140, 120), (140, 155), (140, 190),
                    (140, 225), (140, 260), (140, 320), (140, 365), (140, 410)]
        ftsize_list = [40, 25, 25, 25, 25, 25, 25, 25, 25]
        text_list = [self.grade, self.hp, self.attack, self.defense, self.gold,
                     self.experience, self.yellow, self.blue, self.red]

        return pos_list, ftsize_list, text_list

        disp.show_info(screen, (150, 60), self.grade, size=40)
        disp.show_info(screen, (140, 120), self.hp, size=25)
        disp.show_info(screen, (140, 155), self.attack, size=25)
        disp.show_info(screen, (140, 190), self.defense, size=25)
        disp.show_info(screen, (140, 225), self.gold, size=25)
        disp.show_info(screen, (140, 260), self.experience, size=25)
        disp.show_info(screen, (140, 320), self.yellow, size=25)
        disp.show_info(screen, (140, 365), self.blue, size=25)
        disp.show_info(screen, (140, 410), self.red, size=25)
