import global_var
import config
from time import time, sleep
import random


class Object():

    def __init__(self, character, x, y):
        self._posx = x
        self._posy = y
        self._width = len(character[0])
        self._height = len(character)
        self._shape = character

    ''' code for printing in matrix '''
    def render(self):
        for i in range(self._width):
            for j in range(self._height):
                global_var.mp.matrix[j+self._posy][i +
                                                   self._posx] = self._shape[j][i]

    def xget(self):
        return self._posx

    def yget(self):
        return self._posy

    def xdset(self, x):
        self._posx = x

    def ydset(self, x):
        self._posy = x

    def xset(self, x):
        self._posx += x

    def yset(self, x):
        self._posy += x

    def clear(self):
        for i in range(self._width):
            for j in range(self._height):
                global_var.mp.matrix[j+self._posy][i+self._posx] = " "


class bricks(Object):
    def __init__(self, character, x, y, isUnbreakable, strength, powerup):
        super().__init__(character, x, y)
        self.__unbreakable = isUnbreakable
        self.__strength = strength
        self.__destroyed = 0
        self.__powerup = powerup
        if strength == 5:
            self.__bomb = 1
        else:
            self.__bomb = 0
    
    ''' BONUS IMPLEMENTED ''' 
    def bomb(self):
        return self.__bomb
    
    def getD(self):
        return self.__destroyed

    def getPW(self):
        return self.__powerup
    
    def get_width(self):
        return self._width
    
    def get_break(self):
        return self.__unbreakable

    def dest(self):
        self.__destroyed = 1
        if self.getPW() != -1:
            TPW = PowerUp(config.POWERUPS[self.getPW()],
                          self.xget(), self.yget(), self.getPW())
            global_var.paddle.add_powerup(TPW)

    # changing brick color 
    def __change_brick(self, character):
        super().__init__(character, self.xget(), self.yget())

    def dec_strength(self):

        if self.get_break() == 0:
            global_var.paddle.inc_score(1)
            self.__strength -= 1

            if self.__strength == 0:
                global_var.BROKEN += 1
                self.dest()
                self.clear()

            self.__change_brick(config.Bricks[self.__strength - 1])
    
    def zr_strng(self):
        global_var.BROKEN += 1
        global_var.paddle.inc_score(1)
        self.dest()
        self.clear()


class ball(Object):

    def __init__(self, character, x, y):
        super().__init__(character, x, y)
        self.__speedx = -1
        self.__speedy = -1
        if y == global_var.paddle_ground - 1 and global_var.paddle.xget() <= x and global_var.paddle.xget() >= x:
            self.__release = 0
        else:
            self.__release = 1
        self.__exists = 1
        self.__thru = 0

    def xset(self, x):
        self._posx += x
        if self._posx > config.columns - 2:
            self._posx = config.columns - 2
        elif self._posx < 2:
            self._posx = 2

    def getx_speed(self):
        return self.__speedx

    def gety_speed(self):
        return self.__speedy

    def exists(self):
        return self.__exists
    
    def get_release(self):
        return self.__release
    
    def get_thru(self):
        return self.__thru

    def addy(self, x):
        self.__speedy += x
        if self.gety_speed() <=2 and self.gety_speed() >= -2:
            pass
        else:
            if self.gety_speed() < 0:
                self.__speedy = -2
            elif self.gety_speed() > 0: 
                self.__speedy = 2

    def addx(self, x):
        self.__speedx += x
        if self.getx_speed() <=2 and self.getx_speed() >= -2:
            pass
        else:
            if self.getx_speed() < 0:
                self.__speedx = -2
            elif self.getx_speed() > 0: 
                self.__speedx = 2

    def mulx(self):
        self.__speedx *= -1

    def muly(self):
        self.__speedy *= -1

    def yspeed_set(self, x):
        self.__speedy = x

    def xspeed_set(self, x):
        self.__speedx = x


    def kill(self):
        self.__exists = 0

    def release(self):
        self.__release = 1

    def bound(self):
        self.__release = 0

    def make_thru(self):
        self.__thru = 1
        
    def rm_thru(self):
        self.__thru = 0

    #normal move of ball 
    def move(self):
        if self.yget() > config.BRICKS_Y[3] + 2 and self.yget() < global_var.paddle_ground - 2:
            self.xset(self.getx_speed())
            self.yset(self.gety_speed())
        else:
            self.xset(self.getx_speed())
            if self.gety_speed() > 0:
                self.yset(1)
            elif self.gety_speed() < 0:
                self.yset(-1)

    # initial move of the ball
    def initial_move(self, inp):
        if inp == 'd':
            if global_var.paddle.xget() <= global_var.mp.start_index + config.columns - 4 - global_var.paddle.get_width():
                self.xset(4)

        if inp == 'a':
            if global_var.paddle.xget() > global_var.mp.start_index + 3:
                self.xset(-4)

    # bounded move of the object when '''BOUND POWERUP'''

    def bound_move(self, inp):
        if inp == 'd':
            if global_var.paddle.xget() <= global_var.mp.start_index + config.columns - 5 - global_var.paddle.get_width():
                self.xset(4)

        if inp == 'a':
            if global_var.paddle.xget() > global_var.mp.start_index + 3:
                self.xset(-4)
        if inp == 'r':
            for i in global_var.Balls:
                i.release()
                i.muly()
                i.yset(i.gety_speed())


class PowerUp(Object):
    def __init__(self, character, x, y, number):
        super().__init__(character, x, y)
        self.__number = number
        self.__comp = 0
        self.__dur = 10
        self.__start = 0
        self.__inuse = 0
        self.__tmp = 0
    
    

    def get_comp(self):
        return self.__comp

    def get_use(self):
        return self.__inuse

    def get_number(self):
        return self.__number

    def set_start(self):
        self.__start = time()

    def make_comp(self):
        self.__comp = 1

    def move(self):
        self._posy += 1

    def make_use(self):
        self.__inuse = 1



    def thru_ball(self):
        global_var.paddle.inc_thru()
        for i in global_var.Balls:
            i.make_thru()
        

    def multiply_ball(self):
        if len(global_var.Balls) <= 2:
            tmp = []
            for i in global_var.Balls:
                tmp.append(ball(config.ball, i.xget(), i.yget()))
            for i in tmp:
                global_var.Balls.append(i)

    def shrink_ball(self):
        pass

    def fast_balls(self):
        for i in global_var.Balls:
            if i.gety_speed() > 0:
                i.yspeed_set(2)
            else:
                i.yspeed_set(-2)
            if i.getx_speed() > 0:
                i.xspeed_set(2)
            elif i.getx_speed() < 0:
                i.xspeed_set(-2)

    def dec_ball_speed(self):
        for i in global_var.Balls:
            if i.getx_speed() > 0:
                i.xspeed_set(1)
            elif i.getx_speed() < 0:
                i.xspeed_set(-1)
            if i.gety_speed() > 0:
                i.yspeed_set(1)
            elif i.gety_speed() < 0:
                i.yspeed_set(-1)


    def check_time(self):
        if time() - self.__start >= self.__dur:
            self.make_comp()
            if self.__number == 0:
                global_var.paddle.reset_expand()
            elif self.__number == 1:
                global_var.paddle.reset_shrink()
            elif self.__number == 2:
                self.shrink_ball()
            elif self.__number == 3:
                self.dec_ball_speed()
            elif self.__number == 4:
                if global_var.paddle.get_thru() == 1:
                    for i in global_var.Balls:
                        i.rm_thru()
            elif self.__number == 5:
                for i in global_var.Balls:
                    i.release()
                    if i.yget() == global_var.paddle_ground - 1 and i.gety_speed() > 0:
                        i.yspeed_set(-i.gety_speed())

                    
                global_var.paddle.rm_grab()
            
            global_var.paddle.rm_power(self)
            


class paddle(Object):

    def __init__(self, character, x, y, lives):
        super().__init__(character, x, y)
        self.__lives = 5
        self.__score = 0
        self.__end = 0
        self.__start_time = time()
        self.__wasted_time = 0.0
        self.__spent_time = 0.0
        self.__powerups = []
        self.__level = 1
        self.__shrink = 0
        self.__grab_ball = 0
        self.__thruBall = 0
        self.__grab_pw = 0


    def xset(self, x):
        self._posx += x
        if self._posx > config.columns - 2:
            self._posx = config.columns - 2
        elif self._posx < 2:
            self._posx = 2

    def inc_thru(self):
        self.__thruBall += 1
    
    def dec_thru(self):
        self.__thruBall -= 1
    
    def get_thru(self):
        return self.__thruBall
     # remove unusable power
    def rm_power(self,x):
        self.__powerups.remove(x)
        



    # RESET POWER 

    def reset_power(self):
        for i in self.__powerups:
            if i.get_use() == 1 and i.get_comp() == 0:
                if i.get_number() == 0:
                    print("in reset expand")
                    sleep(2)
                    self.reset_expand()
                elif i.get_number() == 1:
                    self.reset_shrink()
                elif i.get_number() == 2:
                    i.shrink_ball()
                elif i.get_number() == 3:
                    i.dec_ball_speed()
                elif i.get_number() == 4:
                    self.__thruBall = 0
                    for i in global_var.Balls:
                        i.rm_thru()

        self.__powerups.clear()

    # RESET POWER
    
    '''POWER UPS '''
    # POWERUP EXPAND PADDLE
    def expand(self):
        if len(config.paddle[0]) - config.PADDLE_LENGTH >= -2:
            config.paddle[0].append("#")
            config.paddle[0].append("#")
            if self._posx + len(config.paddle[0]) >= config.columns:
                self.xset(-3)
            super().__init__(config.paddle, self._posx, self._posy)

    
    def reset_expand(self):
        if len(config.paddle[0]) - config.PADDLE_LENGTH >= -2:
            config.paddle[0] = config.paddle[0][:(len(config.paddle[0]) - 2)]
            self.clear()
            super().__init__(config.paddle, self.xget(), self.yget())

    # POWERUP SHRINK BALL 

    def shrink(self):
        if abs(len(config.paddle[0]) - config.PADDLE_LENGTH) <= 2:
            config.paddle[0] = config.paddle[0] = config.paddle[0][:(
                len(config.paddle[0]) - 2)]
            self.clear()
            self.__shrink += 1
            super().__init__(config.paddle, self.xget(), self.yget())

    def reset_shrink(self):
        if self.__shrink != 0:
            self.__shrink -= 1
            config.paddle[0].append("#")
            config.paddle[0].append("#")
            if self._posx + len(config.paddle[0]) >= config.columns:
                self.xset(-3)
            super().__init__(config.paddle, self._posx, self._posy)

    # BOUND BALL POWER

    def grab_ball(self):
        self.__grab_pw += 1
        self.__grab_ball = 1
    
    def rm_grab(self):
        self.__grab_pw -= 1
        if self.__grab_pw == 0:
            self.__grab_ball = 0
    
    def grabbed(self):
        return self.__grab_ball
    

    def get_power(self):
        return self.__powerups

    def add_powerup(self, x):
        self.__powerups.append(x)

    def inc_level(self):
        self.__level += 1

    def level(self):
        return self.__level

    def set_spenttime(self):
        self.__spent_time = time() - self.__start_time - self.__wasted_time

    def getend(self):
        return self.__end

    def add_wastedtime(self, x):
        self.__wasted_time += x

    def time(self):
        return self.__spent_time

    def endgame(self):
        self.__end = 1

    def lives(self):
        return self.__lives

    def score(self):
        return self.__score

    def dec_lives(self):
        self.__lives -= 1

    def inc_score(self, x):
        self.__score += x

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def move(self, inp):
        if inp == 'd':
            if self.xget() <= global_var.mp.start_index + config.columns - 5 - self.get_width():
                self.xset(4)

        if inp == 'a':
            if self.xget() > global_var.mp.start_index + 3:
                self.xset(-4)