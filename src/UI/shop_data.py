'''
Created on 20200108
@author zs
'''

shop_info = dict()

shop_info[111002] = dict(
    info_list=("增加 {} 点生命", "增加 {} 点攻击", "增加 {} 点防御", "离开商店"),
    goods_type=("hp", "attack", "defense"),
    goods_addition=(800, 4, 4, ""),
    cost_type="gold",
    cost=(100, 100, 100, 0),
    title="  想要增加你的能力吗？\n如果你有 25 金币，你\n可以任意选择一项："
)

shop_info[111011] = dict(
    info_list=("增加 {} 点生命", "增加 {} 点攻击", "增加 {} 点防御", "离开商店"),
    goods_type=("hp", "attack", "defense"),
    goods_addition=(5000, 20, 20, ""),
    cost_type="gold",
    cost=(25, 25, 25, 0),
    title="  想要增加你的能力吗？\n如果你有 25 金币，你\n可以任意选择一项："
)

shop_info[107005] = dict(
    info_list=("提升 {} 级（需要 {} 点）",  "增加攻击 {}（需要 {} 点）",
               "增加防御 {}（需要 {} 点）", "离开商店"),
    goods_type=("grade", "attack", "defense"),
    goods_addition=(1, 5, 5, ""),
    cost_type="experience",
    cost=(100, 30, 30, 0),
    title="  你好，英雄的人类，只\n要你有足够的经验，我就\n可以让你变的更加强大："
)

shop_info[107013] = dict(
    info_list=("提升 {} 级（需要 {} 点）",
               "增加攻击 {}（需要 {} 点）", "增加防御 {}（需要 {} 点）", "离开商店"),
    goods_type=("grade", "attack", "defense"),
    goods_addition=(3, 20, 20, ""),
    cost_type="experience",
    cost=(100, 30, 30, 0),
    title="  你好，英雄的人类，只\n要你有足够的经验，我就\n可以让你变的更加强大："
)
