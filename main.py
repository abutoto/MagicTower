'''
Created on 20191230
@author abutoto
'''

import sys
import time
import pygame as pg
import pygame.freetype as ft

from src.global_var import global_dict
from conf.sysconf import *
from src.loader import read_image_dict, read_monster
from src.UI.form import Form
from src.UI.map import Map
from src.UI.main_menu import MainMenu
from src.player import Player
from src.function import Function


def init():
    # 游戏初始化
    pg.display.set_caption(GAME_NAME)

    bg_img = pg.image.load(BG_IMAGE)
    bg_img = pg.transform.scale(bg_img, [WIDTH, HEIGHT])
    global_dict["bg_img"] = bg_img

    clock = pg.time.Clock()
    clock.tick(FPS)

    map = Map()
    root_screen.add_child(map)
    player = Player()

    global_dict["map"] = map
    global_dict["activate"] = map.priority
    global_dict["player"] = player
    global_dict["image_dict"] = read_image_dict()
    global_dict["monster_dict"] = read_monster()
    global_dict["image_group_timer"] = IMAGE_GROUP_FPS
    global_dict["image_group"] = IMAGE_GROUP
    global_dict["menu"] = None


def run():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                function.action(event)
                global_dict["move"] = True
            elif event.type == pg.KEYUP:
                global_dict["move"] = False

        if global_dict["move"]:
            key_pressed = pg.key.get_pressed()
            active_keys = [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_SPACE]
            for key in active_keys:
                if key_pressed[key]:
                    function.action(pg.event.Event(pg.KEYDOWN, dict(key=key)))
            global_dict["move"] = False

        global_dict["rootscreen"].flush()
        pg.display.update()


if __name__ == '__main__':
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    root_screen = MainMenu(surface=screen, priority=0)
    init()
    global_dict["rootscreen"] = root_screen
    global_dict["move"] = False

    function = Function()
    run()
