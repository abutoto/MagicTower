'''
Created on 20200108
@author abutoto
'''

# 游戏配置
GAME_NAME = "魔塔" # 游戏名
WIDTH = 800 # 宽度
HEIGHT = 600 # 长度
FPS = 60 # 屏幕刷新频率
IMAGE_GROUP_FPS = 10 # 怪物刷新频率
IMAGE_GROUP = 0 # 怪物图片字典ID
FLOOR = 0 # 初始楼层
BLOCK_NUM = 11 # 地图格子数
BLOCK_SIZE = 46 # 地图格子像素大小
MAP_LEFT = 260 # 地图相对左边距离
MAP_TOP = 50 # 地图相对上面距离
FONT_NAME = "C://Windows//Fonts//msyh.ttc" # 字体
BG_IMAGE = "image/map0/game_bg.png" # 背景图
FLOOR_PATH = "conf/image_id_map.txt" # 地图数据图片对应关系
MONSTER_PATH = "conf/monster.txt" # 怪物数据

# 玩家属性
PLAY_X = 9 # 初始格子位置
PLAY_Y = 5
PLAY_FACE = 1 # 朝向
PLAY_GRADE = 1 # 等级
PLAY_HP = 1000 # HP
PLAY_ATTACK = 10 # 攻击力
PLAY_DEFENSE = 10 # 防御力
PLAY_GOLD = 0 # 钱
PLAY_EXPERIENCE = 0 # 经验
PLAY_YELLOW = 0 # 黄钥匙
PLAY_BLUE = 1 # 蓝钥匙
PLAY_RED = 1 # 红钥匙

# 颜色
WHILE = 255, 255, 255 # 白色
FONT_COLOR = WHILE
FRAME_COLOR = 204, 102, 0 # 边框颜色，橙色
