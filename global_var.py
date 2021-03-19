import board
import objects
import config 
import random

mp = board.Map()

BREAKABLE = 0
BROKEN = 0
paddle_ground = mp.height - len(config.paddle) - 1

paddle_lwall = random.randint(1,config.columns - len(config.paddle[0]) - 1)

paddle = objects.paddle(config.paddle, paddle_lwall, paddle_ground, config.lives)

Balls = []

ball = objects.ball(config.ball, random.randint(paddle.xget(),paddle.xget() + paddle.get_width() - 1) , (paddle_ground - 1) )

Balls.append(ball)

ODD_TIMES = 0

Bullets = []

Bricks = []
unbrick = 0
rainb = 0
RainbowBrick = []
BOMB = []

Ufo = objects.Ufo(config.UFO,config.UFOX,config.UFOY, 11, 2)

for y in range(config.BRICK_INIT_H, config.BRICK_FIN_H, config.BRICK_GAP):
    PWU = -1
    row = []
    # if (y//2)%2 == 0:
    
    for x in range(config.BRICKS_START_X_EVEN, config.BRICKS_END_X_EVEN , config.BRICK_XGAP):
        
        bricktoplace = random.randint(0,3)
        # bricktoplace = 4 # remove this line for randomization
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
            unbrick += 1
            if config.NUMBEROFUNBRICKS < unbrick:
                bricktoplace = 0
                BREAKABLE += 1
                if config.NO_OF_POWERUP > 0:
                    PWU = random.randint(0,10)
                    if PWU <= 6:
                        config.NO_OF_POWERUP -= 1
                    else: 
                        PWU = -1
            else: 
                PWU = -1
        
        # rainbow = 1
        tmp = objects.bricks(config.Bricks[bricktoplace],x,y,(bricktoplace == 3),bricktoplace+1,PWU,rainbow)
        if rainbow == 1:
            RainbowBrick.append(tmp)
        row.append(tmp)
    
    Bricks.append(row)


for y in range(config.BRICK_INIT_H,config.BRICK_INIT_H + config.BRICK_GAP * 2 ,config.BRICK_GAP):
    bricktoplace = 4
    for i in range(3):
        PWU = Bricks[(y-config.BRICK_INIT_H)//config.BRICK_GAP][i].getPW()
        x = Bricks[(y-config.BRICK_INIT_H)//config.BRICK_GAP][i].xget()
        Bricks[(y-config.BRICK_INIT_H)//config.BRICK_GAP][i] = objects.bricks(config.Bricks[bricktoplace],x,y,(bricktoplace == 3),bricktoplace+1,PWU,0)
