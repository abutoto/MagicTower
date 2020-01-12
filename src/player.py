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
        self.prop_dict = dict()

        print("Player")

    def try_fight(self, monster):
        heart = self.get_heart(monster)
        if heart == "???":
            return False
        self.hp -= heart
        self.experience += monster["experience"]
        self.gold += monster["gold"]
        return True

    def get_heart(self, monster):
        h1 = self.attack - monster["defense"]
        h2 = monster["attack"] - self.defense
        if h1 <= 0:
            return "???"
        round = math.ceil((monster["hp"] - h1) / h1)

        if round * h2 >= self.hp:
            return "???"
        else:
            return round * h2

    def get_status(self):
        pos_list = [(170, 70), (200, 120), (200, 155), (200, 190),
                    (200, 225), (200, 260), (170, 320), (170, 365), (170, 410)]
        ftsize_list = [30, 25, 25, 25, 25, 25, 35, 35, 35]
        text_list = [self.grade, self.hp, self.attack, self.defense, self.gold,
                     self.experience, self.yellow, self.blue, self.red]

        return pos_list, ftsize_list, text_list

    def has_prop(self, prop_id):
        return prop_id in self.prop_dict

    def get_prop(self, prop_id):
        self.prop_dict[prop_id] = 1

    def strengthen(self, addition_type, addition):
        if addition_type == "grade":
            self.grade += addition
            self.hp += addition * 800
            self.attack += addition * 5
            self.defense += addition * 5
        elif addition_type == "hp":
            self.hp += addition
        elif addition_type == "attack":
            self.attack += addition
        elif addition_type == "defense":
            self.defense += addition
        elif addition_type == "yellow":
            self.yellow += addition
        elif addition_type == "blue":
            self.blue += addition
        elif addition_type == "red":
            self.red += addition
        elif addition_type == "gold":
            self.gold += addition
