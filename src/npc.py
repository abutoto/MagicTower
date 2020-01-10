'''
Created on 20200101
@author zs
'''

import os
import sys
import pygame

from loader import read_file

class NPC():
    def __init__(self):
        print("NPC")

    def meet(self, npc_id, screen, play, disp):
        print(npc_id)
        offset = (0, 0)
        if npc_id == 105:  # 序章中的仙子
            play.yellow += 1
            disp.dialogue = ["勇士:\n  快走吧，我还要去救被关在这里的公主。"]
            disp.dialogue_pos = 330, 300
            offset = (0, -1)
        elif npc_id >= 106 and npc_id <= 108:  # 商店
            pass
        elif npc_id == 109:  # 经验老人
            pass
        elif npc_id == 110:  # 小偷
            pass
        elif npc_id == 111:  # 公主
            pass
        
        return offset