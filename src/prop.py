'''
Created on 20200101
@author zs
'''

import os
import sys
import pygame

from loader import read_file

class Prop():
    def __init__(self):
        self.prop_dict = dict()
        print("Prop")

    def get_prop(self, prop_id, play):
        print(prop_id)
        self.prop_dict[prop_id] = 1

        if prop_id == 201:  # 黄钥匙
            play.yellow += 1
        elif prop_id == 202:  # 蓝钥匙
            play.blue += 1
        elif prop_id == 203:  # 红钥匙
            play.red += 1
        elif prop_id == 204:  # 红血瓶
            play.hp += 200
        elif prop_id == 205:  # 蓝血瓶
            play.hp += 500
        elif prop_id == 206:  # 蓝宝石
            play.defense += 2
        elif prop_id == 207:  # 红宝石
            play.attack += 3
        elif prop_id == 208:  # 铁剑
            play.attack += 10
        elif prop_id == 209:  # 钢剑
            play.attack += 30
        elif prop_id == 210:  # 圣光剑
            play.attack += 120
        elif prop_id == 211:  # 铁盾
            play.defense += 10
        elif prop_id == 212:  # 钢盾
            play.defense += 30
        elif prop_id == 213:  # 星光盾
            play.defense += 120
        elif prop_id == 216:  # 星光神榔
            pass
        elif prop_id == 217:  # 小飞羽
            play.grade += 1
            self.hp += 1000
            self.attack += 7
            self.defense += 7
        elif prop_id == 218:  # 大飞羽
            play.grade += 3
            self.hp += 3000
            self.attack += 21
            self.defense += 21
        elif prop_id == 219:  # 钥匙盒
            play.yellow += 1
            play.blue += 1
            play.red += 1
        elif prop_id == 220:  # 十字架
            pass
        elif prop_id == 221:  # 金币
            play.gold += 300
        elif prop_id == 222:  # 圣水瓶
            play.hp *= 2
        elif prop_id == 223:  # 炎之灵杖
            pass
        elif prop_id == 224:  # 心之灵杖
            pass

    def have_prop(self, prop_id):
        return prop_id in self.prop_dict

    def use_prop(self, prop_id):
        if prop_id not in self.prop_dict:
            return

        if prop_id == 214:  # 风之罗盘
            pass
        elif prop_id == 215:  # 圣光徽
            pass

    def chose_floor(self, max_floor, disp):
        for floor in range(0, max_floor, 4):
            disp.show_