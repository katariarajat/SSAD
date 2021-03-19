import global_var 
import global_funct
import config
import objects
from global_var import paddle,ball,Bricks,Balls
from os import sys
import board
import inputs 
import random
import time


def update(inp):
    if inp == 'l':
        global_funct.new_level()
    global_var.ODD_TIMES += 1
    # rendering  
    global_funct.rainbow()
    paddle.render()
    
    for i in global_var.BOMB:
        if i.get_exist() == 1:
            i.render()

    for i in Bricks:
        for j in i:
            if j.getD() == 0:
                j.render()
    
    for i in paddle.get_power():
        if i.get_use() == 1 and i.get_comp() == 0:
            i.check_time()
        if i.get_comp() == 0 and i.get_use() == 0:
            i.render()

    for i in Balls:
        if i.exists() == 1:
            i.render()  

    if paddle.level() == 4:
        global_var.Ufo.render()

    for i in global_var.Bullets:
        if i.get_exist() == 1:
            i.render()

    global_funct.print_board()
    

    global_funct.bullet_brick_collision()
    
    global_funct.ball_brick_collision()

    paddle.clear()

    for i in Balls:
        if i.exists() == 1:
            i.clear()

    for i in global_var.Bullets:
        i.clear()

    for i in paddle.get_power():
            i.clear()

    for i in Bricks:
        for j in i:
            j.clear()

    for i in global_var.BOMB:
        if i.get_exist() == 1:
            i.clear()
    
    

    if paddle.level() == 4:
        global_var.Ufo.clear()
        global_funct.bomb_paddle_collision()

    if paddle.level() == 4 and global_var.ODD_TIMES%40 == 0:
        global_funct.shoot_paddle()


    paddle.move(inp)

    for i in global_var.BOMB:
        if i.get_exist() == 1:
            i.ymove()

    for i in global_var.Bullets:
        i.ymove()


    for i in Balls:
        if i.exists() == 1:
            if i.get_release() == 1:
                i.move()
            else:
                i.bound_move(inp)

    if global_var.ODD_TIMES%2 == 0: 
        global_var.Ufo.move()

    if global_var.ODD_TIMES%6 == 0: 
        global_funct.fire_bullet()

    if (global_var.ODD_TIMES)%2 == 0:
        for i in paddle.get_power():
            if i.get_use() == 0:
                i.move()
    global_funct.check_bound()  
    global_funct.powers_check()
    paddle.set_spenttime()
    global_funct.level_check()
    if paddle.level() == 4:
        global_funct.ball_ufo_collision()

if __name__ == '__main__':
    hello = inputs.Get()
    global_funct.initialize()
    while 1:
        inp = inputs.input_to(hello)
        sys.stdout.write("\033c")
        update(inp)
        if inp == 'q' or paddle.getend() == 1:
            break
        