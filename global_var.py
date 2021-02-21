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

Bricks = []

for y in config.BRICKS_Y:
    PWU = -1
    row = []
    # if (y//2)%2 == 0:
    for x in range(6, 103 , 7):
        bricktoplace = random.randint(0,4)
        # bricktoplace = 4 # remove this line for randomization
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
        tmp = objects.bricks(config.Bricks[bricktoplace],x,y,(bricktoplace == 3),bricktoplace+1,PWU)
        row.append(tmp)
    Bricks.append(row)