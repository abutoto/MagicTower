'''
Created on 20191230
@author abutoto
'''

import sys
import pygame as pg
import pygame.freetype as ft

from src.global_var import global_dict
from conf.sysconf import *
from src.loader import read_image_dict, read_monster
from src.UI.form import Form
from src.UI.map import Map
from src.player import Player
from src.action import ActionControl
from src.function import Function

def init():
    pg.display.set_caption(GAME_NAME)

    bg_img = pg.image.load(BG_IMAGE)
    bg_img = pg.transform.scale(bg_img, [WIDTH, HEIGHT])
    bg_img = Form(surface=bg_img)
    bg_img.create_rect((254,44), (772,562), FRAME_COLOR, 0)
    root_screen.add_child(bg_img)

    clock = pg.time.Clock()
    clock.tick(FPS)

    map = Map()
    root_screen.add_child(map)

    player = Player()

    global_dict["map"] = map
    global_dict["player"] = player
    global_dict["image_dict"] = read_image_dict()
    global_dict["monster_dict"] = read_monster()
    global_dict["image_group_timer"] = IMAGE_GROUP_FPS
    global_dict["image_group"] = IMAGE_GROUP
    global_dict["function"] = Function()

    action_control.register_action('QUIT', pg.QUIT, quit)
    action_control.register_action('MOVE', pg.KEYDOWN, global_dict["function"].action)

def run():
    while True:
        action_control.action_render()

        image_group_timer = global_dict["image_group_timer"] - 1
        if image_group_timer == 0:
            image_group_timer = IMAGE_GROUP_FPS
            global_dict["image_group"] = global_dict["image_group"] ^ 1
        global_dict["image_group_timer"] = image_group_timer

        global_dict["function"].update_screen()
        global_dict["rootscreen"].flush()
        global_dict["function"].draw_statusbar()
        pg.display.update()

if __name__ == '__main__':
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    root_screen = Form(surface=screen)
    global_dict["rootscreen"] = root_screen
    action_control = ActionControl()
    init()

    run()

