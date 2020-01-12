'''
Created on 20200111
@author abutoto
'''

import os
import sys
import pygame as pg

from src.UI.menu import *

def get_shop(npc_id, floor):
    shop_image = global_dict.get("image_dict")[0][113]
    info_list = ["增加 {} 点生命", "增加 {} 点攻击", "增加 {} 点防御", "离开商店"]
    goods_type = ["hp", "attack", "defense"]
    goods_addition = [800, 4, 4, ""]
    cost_type = "gold"
    cost = (25, 25, 25, 0)
    if floor == 11:
        goods_addition = [5000, 20, 20, ""]
        cost = (100, 100, 100, 0)
    title = "  想要增加你的能力吗？\n如果你有 {} 金币，你\n可以任意选择一项：".format(cost[0])
    shop = Shop(shop_image=shop_image, title=title, goods_type=goods_type,
                goods_addition=goods_addition, info_list=info_list, cost_type=cost_type, cost=cost)
    
    return shop
