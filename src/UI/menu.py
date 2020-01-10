'''
Created on 20200108
@author zs
'''

import os
import sys
import pygame as pg
import pygame.freetype as ft

from form import Form
from conf.sysconf import *
from src.global_var import global_dict

class Menu(Form):
    def __init__(self):
        super.__init__(self)
        self.activate = False
        self.lock = False

    def action(self, event):
        pass