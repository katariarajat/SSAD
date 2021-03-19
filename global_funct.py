import config
import random
import os
import global_var
from global_var import paddle, ball, mp, paddle_ground,paddle_lwall,Bricks,BREAKABLE,BROKEN,Balls,RainbowBrick
from colorama import Fore, Back, Style
import objects
import time
import inputs
from playsound import playsound 


def create_header():
    if paddle.level() ==4:
        print( "\033[2;1H" + Fore.WHITE + Back.BLUE + Style.BRIGHT + ("  SCORE: " + str(paddle.score()) + "   |  LIVES: " + str(paddle.lives()) + "   |  LEVEL: " + str(paddle.level()) + "   |  TIME: " + str(paddle.time())[:5] + "   |  MONSTOR POWER: " + str(global_var.Ufo.get_power())) .center(config.columns), end='')
        print(Style.RESET_ALL)
    else:
        print( "\033[2;1H" + Fore.WHITE + Back.BLUE + Style.BRIGHT + ("  SCORE: " + str(paddle.score()) + "   |  LIVES: " + str(paddle.lives()) + "   |  LEVEL: " + str(paddle.level()) + "   |  TIME: " + str(paddle.time())[:5]) .center(config.columns), end='')
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
                    playsound('WALLTOUCH.WAV')
                    if i < x_p + (paddle.get_width()) / 2:
                        if paddle.grabbed() == 1:
                            ball.bound() 
                        else:
                            if ball.xget() >= 0:
                                ball.addx(-1)
                            # ball.addx(tmp)
                            ball.muly()        
                    else:
                        if paddle.grabbed() == 1:
                            ball.bound() 
                        else:
                            if ball.xget() <= 0:
                                ball.addx(1)
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
    while len(Balls) != 1:
        Balls.pop()
        
    Balls[0].clear()
    paddle.clear()
    paddle_lwall = random.randint(1,config.columns - paddle.get_width() - 1)
    paddle.xdset(paddle_lwall)
    paddle.ydset(paddle_ground)
    Balls[0].xdset(random.randint(paddle.xget(),paddle.xget() + paddle.get_width() - 1))
    Balls[0].ydset(paddle_ground - 1)
    Balls[0].yspeed_set(-1)
    Balls[0].xspeed_set(1)

def BrickYReset():
    reset_brick_height()
    for i in range(config.BRICK_INIT_H, config.BRICK_FIN_H, config.BRICK_GAP):
        for j in Bricks[(i-config.BRICK_INIT_H)//config.BRICK_GAP]:
            j.clear()
            j.ydset(i)
    

def killed(ball):
    if len(Balls) > 1:
        Balls.remove(ball)      # just remove the ball from queue 

    elif len(Balls) == 1:
        paddle.dec_lives()
        time.sleep(1)
        if paddle.level() != 4:
            BrickYReset()
        if paddle.lives() == 0:
            display_ending()
            return
        Bomb_reset()
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
    for i in global_var.BOMB:
        if i.get_exist() == 1:
            i.render()
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
        # if inp == 'l':
        #     new_level()
        #     return 
        paddle.clear()
        for i in Bricks:
            for j in i:
                j.clear()
        for i in global_var.BOMB:
            if i.get_exist() == 1:
                i.clear()
                i.ymove()
        
        for i in Balls:
            i.clear()
            i.initial_move(inp)

        if paddle.level() == 4:
            global_var.Ufo.clear()
            bomb_paddle_collision()  

        global_var.Ufo.move()
        global_var.ODD_TIMES+=1
        if paddle.level() == 4 and global_var.ODD_TIMES%40 == 0:
            shoot_paddle()

        paddle.move(inp)
        paddle.render()

        if paddle.level() == 4:
            global_var.Ufo.render()

        for i in Bricks:
            for j in i:
                if j.getD() == 0:
                    j.render()

        for i in global_var.BOMB:
            if i.get_exist() == 1:
                i.render()

        for i in Balls:    
            i.render()

        print_board()

        rainbow()

    finaltime = time.time()
    paddle.add_wastedtime(finaltime - initime)
    paddle.clear()
  
    for i in Balls:
        i.clear()
        i.release()
    paddle.set_level_start_time()
    return 


def blast(x):
    
    for i in Bricks:
        for j in i:
            if j.xget() == x.xget() and j.yget() == x.yget() + config.BRICK_GAP and j.getD() == 0:
                j.zr_strng()
                if j.bomb() == 1 :
                    blast(j)
            elif j.xget() == x.xget() and j.yget() == x.yget() - config.BRICK_GAP and j.getD() == 0:
                j.zr_strng()
                if j.bomb() == 1:
                    blast(j)
            elif j.xget() == x.xget() + config.BRICK_XGAP and j.yget() == x.yget() and j.getD() == 0:
                j.zr_strng()
                if j.bomb() == 1:
                    blast(j)
            elif j.xget() == x.xget() - config.BRICK_XGAP and j.yget() == x.yget() and j.getD() == 0:
                j.zr_strng()
                if j.bomb() == 1:
                    blast(j)
            elif j.xget() == x.xget() + config.BRICK_XGAP and j.yget() == x.yget()  + config.BRICK_GAP and j.getD() == 0:
                j.zr_strng()
                if j.bomb() == 1:
                    blast(j)
            elif j.xget() == x.xget() + config.BRICK_XGAP and j.yget() == x.yget()  - config.BRICK_GAP and j.getD() == 0:
                j.zr_strng()
                if j.bomb() == 1:
                    blast(j)
            elif j.xget() == x.xget() - config.BRICK_XGAP and j.yget() == x.yget() + config.BRICK_GAP and j.getD() == 0:
                j.zr_strng()
                if j.bomb() == 1:
                    blast(j)
            elif j.xget() == x.xget() - config.BRICK_XGAP and j.yget() == x.yget() - config.BRICK_GAP and j.getD() == 0:
                j.zr_strng()
                if j.bomb() == 1:
                    blast(j)

def reset_brick_height():
    config.BRICK_INIT_H = config.BRICKS_Y[0]
    config.BRICK_FIN_H = (config.NumberOfBricksRow-1) * config.BRICK_GAP + config.BRICKS_Y[0] + 1


def clear_bricks():
    for i in Bricks:
        for j in i:
            j.clear()

def inc_break_height():
    for i in Bricks:
        for j in i:
            j.yset(1)
    config.BRICK_INIT_H += 1
    config.BRICK_FIN_H += 1

def check_brick_fall():
    if time.time() - paddle.get_level_start_time() > paddle.getBrickFallTime():
        clear_bricks()
        inc_break_height()        
    
    if config.BRICK_FIN_H == paddle.yget() - 1:
        paddle.dec_lives()
        reset()
        reset_brick_height()
        BrickYReset()
        initialize()

def ball_brick_collision():
    
    for ball in Balls:
        for y in range(config.BRICK_INIT_H, config.BRICK_FIN_H , config.BRICK_GAP):
            if ball.yget() == y:
                for x in Bricks[(y-config.BRICK_INIT_H)//config.BRICK_GAP]:
                    if x.getD() == 0:
                        if ball.xget() >= x.xget() and ball.xget() <= x.xget() + x.get_width() - 1:
                            if x.get_break() == 0:
                                playsound('BRICKBREAK.WAV')
                            if ball.get_thru() == 1:
                                x.zr_strng()
                                if x.bomb() == 1:
                                    blast(x)
                            else:
                                if x.getRainbow() == 1:
                                    x.setRainbow(0)    
                                elif x.bomb() == 1:
                                    x.zr_strng()
                                    blast(x)
                                else:
                                    x.dec_strength()
                                ball.muly()
                            if paddle.getFireball() == 1:
                                blast(x)
                            if x.getRainbow() == 1:
                                x.setRainbow(0)
                            check_brick_fall()
    

def ball_ufo_collision():
    for i in Balls:
        if i.yget() <= config.UFOY  and i.yget() >= config.UFOY:
            if i.xget() >= global_var.Ufo.xget() and i.xget() <= global_var.Ufo.xget() + len(config.UFO[0]):
                global_var.Ufo.decPower()
                i.ydset(config.UFOY)
                i.xspeed_set(1)
                i.yspeed_set(1)
        # elif i.yget() == config.UFOY + len(config.UFO[0]) and i.yget() == config.UFOY:
        #     if i.xget() >= global_var.Ufo.xget() and i.xget() <= global_var.Ufo.xget() + len(config.UFO[0]):
        #         global_var.Ufo.decPower()
        #         i.muly()
        if global_var.Ufo.get_defe() == 2:
            if global_var.Ufo.get_power() == 10:
                global_var.Ufo.dec_defe()
                row = []
                for x in range(config.BRICKS_START_X_EVEN, config.BRICKS_END_X_EVEN, config.BRICK_XGAP):
                    tmp = objects.bricks(config.Bricks[0],x,config.BRICK_INIT_H - config.BRICK_GAP ,0,1,-1,0)
                    row.append(tmp)
                config.BRICK_INIT_H = config.BRICK_INIT_H - config.BRICK_GAP
                global_var.Bricks.append(row)

        if global_var.Ufo.get_defe() == 1:
            if global_var.Ufo.get_power() == 2:
                global_var.Ufo.dec_defe()
                row = []
                for x in range(config.BRICKS_START_X_EVEN, config.BRICKS_END_X_EVEN, config.BRICK_XGAP):
                    tmp = objects.bricks(config.Bricks[0],x,config.BRICK_INIT_H - config.BRICK_GAP,0,1,-1,0)
                    row.append(tmp)
                config.BRICK_INIT_H = config.BRICK_INIT_H - config.BRICK_GAP
                global_var.Bricks.append(row)

        if global_var.Ufo.get_power() == 0:
            display_ending()

def rainbow():

    for i in range(len(Bricks)):
        for j in range(len(Bricks[i])):
            if Bricks[i][j].getRainbow() == 1:
                bricktoplace = (Bricks[i][j].getBrick()+1)%5
                PWU = Bricks[i][j].getPW()
                x = Bricks[i][j].xget()
                y = Bricks[i][j].yget()
                tmp = objects.bricks(config.Bricks[bricktoplace],x,y,(bricktoplace == 3),bricktoplace+1,PWU,1)         
                Bricks[i][j] = tmp

def Bomb_reset():
    for i in global_var.BOMB:
        i.kill()
    global_var.BOMB.clear()

def shoot_paddle():
    print(global_var.Ufo.xget(), global_var.paddle.xget())
    # if (global_var.Ufo.xget())+len(config.UFO[0])//2 >= paddle.xget() and (global_var.Ufo.xget()) + len(config.UFO[0])/2 <= paddle.xget():
    # print("hello")
    # time.sleep(2) 
    tmp = objects.Bomb(config.Bomb,global_var.Ufo.xget()+len(config.UFO[0])//2,config.UFOY+len(config.UFO))    
    global_var.BOMB.append(tmp)

def bomb_paddle_collision():
    for i in global_var.BOMB:
        if i.yget() == global_var.paddle.yget() - 1 and i.xget() >= global_var.paddle.xget() and i.xget() <= global_var.paddle.xget() + paddle.get_width():
            paddle.dec_lives()
            reset()
            Bomb_reset()

def boss_level():
    clear_bricks()
    config.NO_OF_POWERUP = 0
    config.NUMBEROFUNBRICKS = 10
    config.BRICK_GAP = 2
    config.BRICK_XGAP = 10
    config.NumberOfBricksRow = 2
    global_var.paddle.setBrickFallTime(1000)
    config.BRICK_INIT_H = config.UFOY + config.HeightofUfo + 8
    config.BRICK_FIN_H = (config.NumberOfBricksRow-1) * config.BRICK_GAP + config.BRICK_INIT_H + 1
    Bricks.clear()
    for y in range(config.BRICK_INIT_H, config.BRICK_FIN_H , config.BRICK_GAP):
        row = []
        for x in range(config.BRICKS_START_X_EVEN, config.BRICKS_END_X_EVEN , config.BRICK_XGAP):
            bricktoplace = 3
            if random.randint(0,20)  < 7:
                tmp = objects.bricks(config.Bricks[bricktoplace],x,y,(bricktoplace == 3),bricktoplace+1,-1,0)
                row.append(tmp)
        Bricks.append(row)
    paddle.set_level_start_time()
    reset()
    paddle.reset_power()
    print(Fore.CYAN + Style.BRIGHT + ("LEVEL : " + str(paddle.level())).center(config.columns))
    print(Style.RESET_ALL)
    # time.sleep(1)
    initialize()

def new_level():

    paddle.inc_level()
    if paddle.level() == 4:
        boss_level()
        print("returened")
        # time.sleep(2)
        return 
    config.NO_OF_POWERUP -= 2
    config.NUMBEROFUNBRICKS += 2
    config.NumberOfBricksRow += 1
    paddle.set_level_start_time()
    clear_bricks()
    reset_brick_height()
    new_bricks()
    reset()
    paddle.reset_power()
    print(Fore.CYAN + Style.BRIGHT + ("LEVEL : " + str(paddle.level())).center(config.columns))
    print(Style.RESET_ALL)
    time.sleep(1)
    initialize()

def new_bricks():

    BREAKABLE = 0
    BROKEN = 0
    paddle.set_level_start_time()

    clear_bricks()

    Bricks.clear()
    
    unbreak = 0
    rainb = 0
    for y in range(config.BRICK_INIT_H, config.BRICK_FIN_H , config.BRICK_GAP):
        row = []
        # if (y//2)%2 == 0:
        for x in range(config.BRICKS_START_X_EVEN, config.BRICKS_END_X_EVEN , config.BRICK_XGAP):
            bricktoplace = random.randint(0,3)
            if config.NUMBEROFRAINBOW > rainb:
                rainb += 1
                rainbow = random.randint(0,1)
            else:
                rainbow = 0

            if bricktoplace != 3:
                BREAKABLE += 1
                if config.NO_OF_POWERUP > 0:
                    PWU = random.randint(0,10)
                    if PWU < 6:
                        config.NO_OF_POWERUP -= 1
                    else: 
                        PWU = -1
                else: 
                    PWU = -1
            else:
                unbreak+=1
                if config.NUMBEROFUNBRICKS < unbreak:
                    bricktoplace = 0
                    BREAKABLE += 1
                    if config.NO_OF_POWERUP > 0:
                        PWU = random.randint(0,10)
                        if PWU < 6:
                            config.NO_OF_POWERUP -= 1
                        else: 
                            PWU = -1
                else: 
                    PWU = -1

            tmp = objects.bricks(config.Bricks[bricktoplace],x,y,(bricktoplace == 3),bricktoplace+1,-1,rainbow)
            row.append(tmp)
        Bricks.append(row)

def fire_bullet():
    if paddle.getBulletPower() == 1:
        tmp = objects.Bullets(config.BULLET, paddle.xget(),paddle.yget() -1)
        global_var.Bullets.append(tmp)
        tmp = objects.Bullets(config.BULLET, paddle.xget()+paddle.get_width(),paddle.yget() -1)
        global_var.Bullets.append(tmp)

def bullet_brick_collision():
    for i in global_var.Bullets:
        for y in range(config.BRICK_INIT_H, config.BRICK_FIN_H , config.BRICK_GAP):
            if i.yget() == y:
                for x in Bricks[(y-config.BRICK_INIT_H)//config.BRICK_GAP]:
                    if x.getD() == 0:
                        if i.xget() >= x.xget() and i.xget() <= x.xget() + x.get_width() - 1:
                                if(x.getRainbow()) == 1:
                                    x.setRainbow(0)
                                else:
                                    x.dec_strength()
                                i.bullet_des()        

def level_check():
    print(BROKEN,BREAKABLE)
    if BROKEN == BREAKABLE:
        paddle.inc_level()
        new_level()
        

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
                elif i.get_number() == 6:
                    paddle.fireball()
                elif i.get_number() == 7:
                    paddle.setbulletPower()
            else:
                i.make_comp()
                i.make_use()
                paddle.rm_power(i)
                
                