import config
import random
import os
from global_var import paddle, ball, mp, paddle_ground,paddle_lwall,Bricks,BREAKABLE,BROKEN,Balls
from colorama import Fore, Back, Style
import objects
import time
import inputs


def create_header():
    print( "\033[2;1H" + Fore.WHITE + Back.BLUE + Style.BRIGHT + ("  SCORE: " + str(paddle.score()) + "   |  LIVES: " + str(paddle.lives())) + "   |  TIME: " + str(paddle.time())[:5] .center(config.columns), end='')
    print(Style.RESET_ALL)

def print_board():
    create_header()
    mp.render()
    

def display_ending():
    os.system('tput reset')
    print(Fore.CYAN + Style.BRIGHT + "FINAL STANDINGS:".center(config.columns))
    print(Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + ("SCORE: " + str(paddle.score())).center(config.columns))
    print(Style.RESET_ALL)
    time.sleep(2)
    paddle.endgame()
    return




def check_bound():

    x_p = paddle.xget()
    y_p = paddle.yget()
    for ball in Balls:
        x_b = ball.xget()
        y_b = ball.yget()
        i = x_p
        middle = (paddle.get_width())//2
        if y_p == y_b + 1:
            while i < x_p + paddle.get_width():
                if x_b == i:
                    tmp = (i-middle-x_p)//2
                    if tmp >= 2:
                        tmp = 2
                    elif tmp <= -2:
                        tmp = -2    
                    
                    if paddle.grabbed() == 1:
                        ball.bound() 
                    else:
                        ball.addx(tmp)
                        ball.muly()        
                    break
                i += 1

        if y_b >= paddle_ground:
            killed(ball)
        
        if ball.xget() >= config.columns - 2:
            ball.mulx()    

        if ball.yget() <= 4:
            ball.muly()

        if ball.xget() <= 2:
            ball.mulx()


def reset():
    Balls[0].clear()
    paddle.clear()
    paddle_lwall = random.randint(1,config.columns - paddle.get_width() - 1)
    paddle.xdset(paddle_lwall)
    paddle.ydset(paddle_ground)
    Balls[0].xdset(random.randint(paddle.xget(),paddle.xget() + paddle.get_width() - 1))
    Balls[0].ydset(paddle_ground - 1)
    Balls[0].yspeed_set(-1)
    Balls[0].xspeed_set(1)

def killed(ball):
    if len(Balls) > 1:
        Balls.remove(ball)

    elif len(Balls) == 1:
    
        paddle.dec_lives()
        time.sleep(1)
        
        if paddle.lives() == 0:
            display_ending()
            return
        reset()
        initialize()    

def initialize():
    hello = inputs.Get()
    paddle.reset_power()
    paddle.render()
    for i in Bricks:
        for j in i:
            if j.getD() == 0:
                j.render()
    for i in Balls:
        i.render()
    print_board()
    inp = 'p'
    initime = time.time()
    while inp != 'r':
        inp = inputs.input_to(hello)
        os.sys.stdout.write("\033c")
        # if inp == 'q':
        #     return 1
        paddle.clear()
        for i in Bricks:
            for j in i:
                j.clear()
        for i in Balls:
            i.clear()
            i.initial_move(inp)
        paddle.move(inp)
        paddle.render()
        for i in Bricks:
            for j in i:
                if j.getD() == 0:
                    j.render()
        for i in Balls:    
            i.render()
        print_board()
    finaltime = time.time()
    paddle.add_wastedtime(finaltime - initime)
    paddle.clear()
    for i in Balls:
        i.clear()
        i.release()
    return 


def blast(x):
    
    for i in Bricks:
        for j in i:
            if j.xget() == x.xget() and j.yget() == x.yget() + 2:
                j.zr_strng()
            elif j.xget() == x.xget() and j.yget() == x.yget() - 2:
                j.zr_strng()
            elif j.xget() == x.xget() + len(config.Bricks[0][0]) + 1 and j.yget() == x.yget() :
                j.zr_strng()
            elif j.xget() == x.xget() - len(config.Bricks[0][0]) - 1 and j.yget() == x.yget() :
                j.zr_strng()
            elif j.xget() == x.xget() + len(config.Bricks[0][0]) + 1 and j.yget() == x.yget()  + 2:
                j.zr_strng()
            elif j.xget() == x.xget() + len(config.Bricks[0][0]) + 1 and j.yget() == x.yget()  - 2:
                j.zr_strng()
            elif j.xget() == x.xget() - len(config.Bricks[0][0]) - 1 and j.yget() == x.yget() + 2:
                j.zr_strng()
            elif j.xget() == x.xget() - len(config.Bricks[0][0]) - 1 and j.yget() == x.yget() - 2:
                j.zr_strng()


def ball_brick_collision():
    
    for ball in Balls:
        for y in range(5,12,2):
            if ball.yget() == y:
                for x in Bricks[(y-5)//2]:
                    if x.getD() == 0:
                        if ball.xget() >= x.xget() and ball.xget() <= x.xget() + x.get_width() - 1:
                            if ball.get_thru() == 1:
                                if x.bomb() == 1:
                                    blast(x)
                                x.zr_strng()
                            else:
                                if x.bomb() == 1:
                                    blast(x)
                                    x.zr_strng()
                                else:
                                    x.dec_strength()
                                ball.muly()


def new_level():

    # BRICK RESET
    Bricks = []
    BREAKABLE = 0
    BROKEN = 0
    for y in config.BRICKS_Y:
        row = []
        if (y//2)%2 == 0:
            for x in range(6, 103 , 7):
                bricktoplace = random.randint(0,3)
                if bricktoplace == 3:
                    BREAKABLE += 1
                tmp = objects.bricks(config.Bricks[bricktoplace],x,y,(bricktoplace == 3),bricktoplace+1,-1)
                row.append(tmp)
        else:
            for x in range(12, 97, 7):

                bricktoplace = random.randint(0,3)
                if bricktoplace == 3:
                    BREAKABLE += 1
                tmp = objects.bricks(config.Bricks[bricktoplace],x,y,(bricktoplace == 3),bricktoplace+1,-1)
                row.append(tmp)
        
        Bricks.append(row)
    
    reset()



def level_check():

    if BROKEN == BREAKABLE:
        paddle.inc_level()
        new_level()
        print(Fore.CYAN + Style.BRIGHT + "LEVEL : " + paddle.level().center(config.columns))
        print(Style.RESET_ALL)
        initialize()

def powers_check():

    for i in paddle.get_power():
        if i.get_use() == 0 and i.yget() == paddle_ground:
            if i.xget() >= paddle.xget() and i.xget() <= (paddle.xget() + paddle.get_width() - 1):
                i.set_start()
                i.make_use()
                if i.get_number() == 0:
                    paddle.expand()
                elif i.get_number() == 1:
                    paddle.shrink()
                elif i.get_number() == 2:
                    i.multiply_ball()
                elif i.get_number() == 3:
                    i.fast_balls()
                elif i.get_number() == 4:
                    i.thru_ball()
                elif i.get_number() == 5:
                    paddle.grab_ball()
            else:
                i.make_comp()
                i.make_use()
                paddle.rm_power(i)
                
                