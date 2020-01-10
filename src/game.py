class Game():
    def __init__(self):
        pygame.init()
        # 屏幕大小
        self.size = width, height = 800, 600
        #self.size = width, height = 1296, 936
        self.screen = pygame.display.set_mode(self.size)

        # 标题
        pygame.display.set_caption("我的魔塔")
        #icon = pygame.image.load("logo")
        # pygame.display.set_icon(icon)

        # 背景图
        self.game_bg = pygame.image.load("image/map0/game_bg.png")
        self.zoom = self.game_bg.get_size(
        )[0] / width, self.game_bg.get_size()[1] / height
        self.game_bg = pygame.transform.scale(self.game_bg, (width, height))

        # 屏幕刷新频率
        self.fps = 60
        self.fclock = pygame.time.Clock()

        self.show_pos = 50, 260  # 游戏区相对左上角位置
        self.cell_size = 46  # 一小格大小
        self.floor_id = 0   # 楼层
        self.img_pos = 0 # 控制动画
        self.img_pos_limit = 20 # 控制动画频率
        self.is_interaction = False # 是否在交互
        
        self.load = Game_Load() # 加载数据类
        self.img_dict = self.load.read_image_dict(self.cell_size)  # 加载所有图片
        self.floor_dict, self.floor_pos = self.load.read_floor()  # 加载地图，玩家初始位置
        self.monster_dict = self.load.read_monster()  # 加载怪物信息

        self.play = Player()  # 玩家
        font_style = "C://Windows//Fonts//msyh.ttc"  # 字体
        white = 255, 255, 255  # 字体颜色
        frame_color = 204, 102, 0  # 边框颜色
        self.disp = Displayer(frame_color, self.cell_size)  # 显示输出类
        self.disp.set_font(font_style, white, 36)
        self.disp.set_dialogue(white, (380, 100), 25, self.img_dict[0][0])

        self.prop = Prop()  # 道具类
        self.npc = NPC()  # NPC类

        self.disp.show_frame(self.game_bg, (257, 47, 512, 512), 5)  # 边框线

    def start(self):
        pygame.event.set_allowed(pygame.KEYDOWN)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PAGEUP:
                        if self.is_interaction:
                            continue
                        self.move_floor(1)
                    elif event.key == pygame.K_PAGEDOWN:
                        if self.is_interaction:
                            continue
                        self.move_floor(-1)
                    elif event.key == pygame.K_UP:
                        if self.is_interaction:
                            continue
                        self.move(0)
                    elif event.key == pygame.K_DOWN:
                        if self.is_interaction:
                            continue
                        self.move(1)
                    elif event.key == pygame.K_LEFT:
                        if self.is_interaction:
                            continue
                        self.move(2)
                    elif event.key == pygame.K_RIGHT:
                        if self.is_interaction:
                            continue
                        self.move(3)
                    elif event.key == pygame.K_w:
                        if self.is_interaction == False:
                            continue
                        pass
                    elif event.key == pygame.K_s:
                        if self.is_interaction == False:
                            continue
                        pass
                    elif event.key == pygame.K_a:
                        if self.is_interaction == False:
                            continue
                        pass
                    elif event.key == pygame.K_d:
                        if self.is_interaction == False:
                            continue
                        pass
                    elif event.key == pygame.K_SPACE:
                        if self.is_interaction == False:
                            continue
                        pass
                    elif event.key == pygame.K_l:
                        if self.prop.have_prop(215) == False:
                            continue
                        pass
                    elif event.key == pygame.K_j:
                        if self.prop.have_prop(214) == False:
                            continue
                        pass

            self.update_game()

    def update_game(self):
        self.screen.fill(0)
        self.screen.blit(self.game_bg, (0, 0))

        img_dict = self.img_dict[1 if self.img_pos *
                                 2 >= self.img_pos_limit else 0]
        # 画地图
        self.disp.show_floor(self.game_bg,
                             self.floor_dict[self.floor_id],
                             img_dict,
                             self.show_pos,
                             self.cell_size)

        # 画玩家
        play_id = self.play.face + 101
        player_pos = self.show_pos[1] + self.cell_size * \
            self.play.pos_y, self.show_pos[0] + self.cell_size * self.play.pos_x
        self.disp.show_cell(self.screen, img_dict[play_id], player_pos)
        # 左边栏玩家信息
        self.play.show(self.screen, self.disp)

        # 显示层
        self.disp.show_info(self.screen, (122, 467), self.floor_id)

        # 显示对话
        #self.is_interaction = self.disp.show_dialogue(self.game_bg)

        pygame.display.update()
        self.fclock.tick(self.fps)
        self.img_pos = (self.img_pos + 1) % self.img_pos_limit

    def move_floor(self, floor_id, jump=False):
        if not jump:
            if self.floor_id + floor_id not in self.floor_dict:
                return
            self.floor_id += floor_id
            self.play.pos_x, self.play.pos_y = self.floor_pos[self.floor_id][
                :2] if floor_id > 0 else self.floor_pos[self.floor_id][2:]
        else:
            self.play.pos_x, self.play.pos_y = self.floor_pos[self.floor_id][
                :2] if floor_id <= self.floor_id else self.floor_pos[self.floor_id][2:]
            self.floor_id = floor_id
        self.play.face = 1

    def change_cell(self, id, pos=None):
        if pos:
            if pos[0] < 0 or pos[0] >= 11 or pos[1] < 0 or pos[1] >= 11:
                return
            self.floor_dict[self.floor_id][pos[0]][pos[1]] = id
        else:
            self.floor_dict[self.floor_id][self.play.pos_x][self.play.pos_y] = id

    def move(self, flag):
        go = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        last_pos = self.play.pos_x, self.play.pos_y
        move_to = self.play.pos_x + go[flag][0], self.play.pos_y + go[flag][1]
        self.play.pos_x, self.play.pos_y = move_to
        self.play.face = flag
        if not self.check_move(move_to):
            self.play.pos_x, self.play.pos_y = last_pos

    def check_move(self, pos):
        if pos[0] < 0 or pos[0] >= 11 or pos[1] < 0 or pos[1] >= 11:
            return False

        move_id = self.floor_dict[self.floor_id][pos[0]][pos[1]]
        status = False
        if move_id < 0:  # 不可走区域
            pass
        elif move_id == 0:  # 路
            status = True
        elif move_id < 100:  # 门
            status = self.check_door(move_id)
        elif move_id < 200:  # npc
            offset = self.npc.meet(move_id, self.game_bg, self.play, self.disp)
            if offset != (0, 0):
                self.change_cell(0)
                self.change_cell(
                    move_id, (pos[0] + offset[0], pos[1] + offset[1]))
            status = True
        elif move_id < 300:  # 道具
            self.prop.get_prop(move_id, self.play)
            self.change_cell(0)
            status = True
        elif move_id >= 300:  # 怪物
            status = self.fight(move_id)
            if status:
                self.change_cell(0)

        return status

    def check_door(self, move_id):
        status = False
        if move_id == 1:  # 上楼
            self.move_floor(1)
            status = True
        elif move_id == 2:  # 下楼
            self.move_floor(-1)
            status = True
        elif move_id == 3:  # 黄门
            if self.play.yellow > 0:
                self.play.yellow -= 1
                self.change_cell(0)
                status = True
        elif move_id == 4:  # 蓝门
            if self.play.blue > 0:
                self.play.blue -= 1
                self.change_cell(0)
                status = True
        elif move_id == 5:  # 红门
            if self.play.red > 0:
                self.play.red -= 1
                self.change_cell(0)
                status = True
        elif move_id == 6:  # 二层门
            if self.prop.have_prop(216):
                self.change_cell(0)
                status = True
        elif move_id == 7:  # 不可开护栏门
            pass
        elif move_id == 8:  # 可开护栏门
            self.change_cell(0)
            status = True
        return status

    def fight(self, monster_id):
        status = self.play.try_fight(self.monster_dict[monster_id - 300])
        return status
    
    def interaction(self):
        pygame.event.set_allowed()

