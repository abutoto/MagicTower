'''
Created on 20200101
@author abutoto
'''

import os
import sys
import pygame
import pygame.freetype


from loader import read_file


class Displayer():
    def __init__(self, frame_color, cell_size):
        self.frame_color = frame_color
        self.cell_size = cell_size

        print("Displayer")

    def set_font(self, font_style, white=(255, 255, 255), size=36):
        self.font = pygame.freetype.Font(font_style, size)
        self.color = white

    def set_dialogue(self, dialogue_color, dialogue_size, dialogue_font_size, dialogue_bg):
        self.dialogue = list()
        self.dialogue_pos = (0, 0)
        self.dialogue_color = dialogue_color
        self.dialogue_size = (380, 100)
        self.dialogue_font_size = 25
        self.dialogue_bg = dialogue_bg

    def show_floor(self, screen, floor, img_dict, pos, cell_size):
        x = 0
        for i in floor:
            y = 0
            for j in i:
                screen.blit(img_dict[j], (y + pos[1], x + pos[0]))
                y += cell_size
            x += cell_size

    def show_cell(self, screen, img, pos):
        # print(pos)
        screen.blit(img, pos)

    def show_info(self, screen, pos, info, color=None, size=25):
        info = str(info)
        color = color if color else self.color
        self.font.render_to(screen, pos, info, fgcolor=color, size=size)

    def show_message(self, screen, pos, message, color=None, size=25):
        info = str(info)
        color = color if color else self.color
        self.font.render_to(screen, pos, info, fgcolor=color, size=size)

    def show_frame(self, screen, frame_info, frame_size):
        pygame.draw.rect(
            screen,
            self.frame_color,
            frame_info,
            frame_size)  # 边框线

    def show_dialogue(self, screen):
        status = False
        if len(self.dialogue) > 0:
            status = True
            fontsf = pygame.Surface(self.dialogue_size)
            for i in range(3, self.dialogue_size[0], self.cell_size):
                for j in range(3, self.dialogue_size[1], self.cell_size):
                    fontsf.blit(self.dialogue_bg, (i, j))
            pygame.draw.rect(fontsf, self.frame_color,
                             (0, 0) + self.dialogue_size, 5)  # 边框线

            font_rect = self.font.render_to(
                fontsf,
                (10, 10),
                self.dialogue[0],
                fgcolor=self.dialogue_color,
                size=self.dialogue_font_size)

            screen.blit(fontsf, self.dialogue_pos)
            #self.dialogue = self.dialogue[1:]
        
        return status