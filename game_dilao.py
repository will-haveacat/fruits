'''
运行后，按下空格键开始游戏，键盘的上下左右键操作左上方人物的移动
右下方的人物，表示终点
人物在移动过程中，如果碰到了怪物或者子弹（没错，在飞的小东西就是子弹），就会扣分
左上角的score是得分
只要到达终点，就会显示“YOU WIN”，此时，等待一会，界面自动关闭
'''
import pygame as pg
from time import sleep
from math import atan, sin, cos

# 加载元素的函数
def create_element(path, width, high, is_alpha):
    if is_alpha:
        a = pg.image.load(path).convert_alpha()
    else:
        a = pg.image.load(path).convert()
    a = pg.transform.scale(a, (width, high))
    return a

# 角色基本的设置、参数
screen_width = 1000
screen_high = 600
pg.init()
screen = pg.display.set_mode((screen_width, screen_high))
pg.display.set_caption('title')
x = 200
y = 0
x_friend, y_friend = 950, 550
x_eny = 350
y_eny = 150
x_monkey = 200
y_monkey = 300
step = 20
step_eny = 1
step_monkey = 10
step_fire = 3
is_start = False
is_end = False
is_win = False
scoreInt = 10
pear_width = 30
pear_high = 30
enemy_monkey_width = 80
enemy_monkey_high = 80
enemy_shoter_width = 50
enemy_shoter_high = 50
fire_width, fire_high = 15, 15
x_fire, y_fire = 800, 170
stone_width = 50
stone_high = 50
font1 = pg.font.SysFont('宋体', 30, True)  # 文字（得分）

clock = pg.time.Clock()

# 加载图片
pear = create_element(path='./image/pear.png', width=pear_width, high=pear_high, is_alpha=True)
friend = create_element(path='./image/pear.png', width=pear_width, high=pear_high, is_alpha=True)
shoter = create_element(path='./image/enemy_shoter.jpg', width=enemy_shoter_width, high=enemy_shoter_high,
                        is_alpha=True)
enemy = create_element(path='./image/enemy_ball.jpg', width=pear_width, high=pear_high, is_alpha=True)
enemy_monkey = create_element('./image/enemy_monkey.jpg', enemy_monkey_width, enemy_monkey_high, True)
bg2 = create_element('./image/background.jpg', screen_width, screen_high, False)
bg_win = create_element('./image/bg_win.jpg', screen_width, screen_high, False)
stone = create_element('./image/sub_bg.png', stone_width, stone_high, True)
fire = create_element('./image/fire.jpg', fire_width, fire_high, True)

# 射击者（一种敌人）的设置
x_shoter, y_shoter = 800, 150
init_fire_pos = (x_shoter - 10, y_shoter + 15)  # fire(一种子弹)的初始位置

# rect
pear_rect = pg.Rect.move(pear.get_rect(), x, y)
fri_rect = pg.Rect.move(friend.get_rect(), x_friend, y_friend)
shoter_rect = pg.Rect.move(shoter.get_rect(), x_shoter, y_shoter)
enemy_rect = pg.Rect.move(enemy.get_rect(), x_eny, y_eny)
monkey_rect = pg.Rect.move(enemy_monkey.get_rect(), x_monkey, y_monkey)
fire_rect = pg.Rect.move(fire.get_rect(), x_fire, y_fire)
fire_rect0 = fire_rect

stone_position = [pg.Rect(0, 0, 100, 600), pg.Rect(300, 0, 700, 150), pg.Rect(400, 200, 600, 50),
                  pg.Rect(600, 250, 400, 50), pg.Rect(200, 400, 70, 200),
                  pg.Rect(150, 0, 50, 300), pg.Rect(250, 0, 50, 150), pg.Rect(250, 200, 50, 100),
                  pg.Rect(150, 400, 50, 100),
                  ]  # 石头1

# print(pear_rect.collidelist(stone_position)) # 没重合 返回-1 ；重合 返回1

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:  # 按下空格游戏开始
                is_start = True

        # 游戏开始
        if is_start:
            is_end = False
            while True:
                # enemy白球转弯、移动
                if x_eny > 400 or x_eny < 200:
                    step_eny = step_eny * (-1)
                x_eny += step_eny
                enemy_rect = pg.Rect.move(enemy_rect, step_eny, 0)

                # enemy_monkey转弯、移动
                if x_monkey < 200 or x_monkey > 500:
                    step_monkey *= (-1)
                x_monkey += step_monkey
                monkey_rect = pg.Rect.move(monkey_rect, step_monkey, 0)

                # 子弹转弯、移动
                if x_fire < -200 or x_fire > screen_width or y_fire < 0 or y_fire > screen_high:
                    x_fire = x_shoter
                    fire_rect = fire_rect0
                else:
                    x_fire -= step_fire
                fire_rect = pg.Rect.move(fire_rect, (-1) * step_fire, 0)

                clock.tick(60)
                # pear移动量
                move_x = 0
                move_y = 0
                if is_end:
                    break
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        is_start = False
                    if event.type == pg.KEYDOWN:  # 使用了键盘
                        temp_rect = pear_rect  # 记录pear_rect初试状态

                        if event.key == pg.K_LEFT:
                            move_x = -1 * step
                        elif event.key == pg.K_RIGHT:
                            move_x = step
                        elif event.key == pg.K_UP:
                            move_y = -1 * step
                        elif event.key == pg.K_DOWN:
                            move_y = step
                        pear_rect = pg.Rect.move(pear_rect, move_x, move_y)

                        # 碰撞检测
                        # print(pear_rect.collidelist(stone_position))  # 为-1时，才可以继续移动
                        if pear_rect.collidelist(stone_position) != -1:  # rect[0]:x   rect[1]:y
                            # print(pear_rect[1])
                            move_y, move_x = 0, 0
                            pear_rect = temp_rect
                        # print("pear enemy",pear_rect.colliderect(enemy_rect))# 总是-1
                        # print("pear_rect y:", pear_rect[1])
                        # print("enemy_rect y:", enemy_rect[1])
                        # print("pear_rect x:", pear_rect[0])
                        # 撞到敌人或子弹，就扣分
                        if pear_rect.colliderect(enemy_rect) or pear_rect.colliderect(monkey_rect) or \
                                pear_rect.colliderect(shoter_rect) or pear_rect.colliderect(fire_rect):
                            move_y, move_x = 0, 0
                            pear_rect = temp_rect
                            scoreInt -= 1  # 扣分
                        # 边界（游戏界面的边界）检测
                        if pear_rect[0] <= 0 or pear_rect[0] >= screen_width or pear_rect[1] <= 0 or \
                                pear_rect[1] >= screen_high:
                            move_y, move_x = 0, 0
                            pear_rect = temp_rect

                    x = x + move_x
                    y = y + move_y

                    # 赢了
                    if pear_rect.colliderect(fri_rect):
                        print('you win')
                        is_win = True
                        is_end = True
                        is_start = False

                    # if y > screen_high and x > screen_width:
                    #     print('you win')
                    #     is_win = True
                    #     is_end = True
                    #     is_start = False
                    # # 石头的限制
                    # if x > 200:
                    #     x -= move_x
                    # if x < 200:
                    #     x -= move_x
                screen.blit(bg2, (0, 0))  # 清除残影

                # 布置石头  # 石头2
                for i in range(14):
                    screen.blit(stone, (200 + i * 50, 400))
                    screen.blit(stone, (200 + i * 50, 450))
                    screen.blit(stone, (200 + i * 50, 500))
                    screen.blit(stone, (200 + i * 50, 550))
                for i in range(12):
                    screen.blit(stone, (400 + i * 50, 200))
                for i in range(8):
                    screen.blit(stone, (600 + i * 50, 250))
                for i in range(14):
                    screen.blit(stone, (300 + i * 50, 0))
                    screen.blit(stone, (300 + i * 50, 50))
                    screen.blit(stone, (300 + i * 50, 100))
                for i in range(12):
                    screen.blit(stone, (0, i * 50))
                    screen.blit(stone, (50, i * 50))
                    screen.blit(stone, (100, i * 50))
                for i in range(6):
                    screen.blit(stone, (150, i * 50))
                for i in range(3):
                    screen.blit(stone, (250, i * 50))
                for i in range(2):
                    screen.blit(stone, (250, 200 + i * 50))
                for i in range(4):
                    screen.blit(stone, (150, 400 + i * 50))

                screen.blit(pear, (x, y))  # 画人物
                screen.blit(enemy, (x_eny, y_eny))  # 敌人：white_ball
                screen.blit(enemy_monkey, (x_monkey, y_monkey))  # 敌人：enemy_monkey
                screen.blit(friend, (screen_width - pear_width, screen_high - pear_high))  # 朋友（终点）
                screen.blit(shoter, (x_shoter, y_shoter))  # 敌人：enemy_shoter
                screen.blit(fire, (x_fire, y_fire))  # 攻击物：fire子弹

                # 显示得分
                score = font1.render('score:' + str(scoreInt), True, [255, 255, 255])
                screen.blit(score, [20, 20])

                pg.display.update()

    if is_win:
        screen.blit(bg_win, (0, 0))  # 加载“you win”界面
    else:
        screen.blit(bg2, (0, 0))  # 加载普通界面

    pg.display.update()
    if is_end:
        sleep(2)
        exit()
