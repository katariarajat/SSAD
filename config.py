import os
import sys
import random
import termios, tty, time
from colorama import init, Fore, Back, Style
import objects
from math import pi
import numpy as np 


columns = 110
rows = 35

lives = 5

paddle = [["#","#","#","#","#","#","#","#","#","#","#"]]
ball = [["@"]]
Bricks = [[["1","1","1","1","1","1"]],[["2","2","2","2","2","2"]],[["3","3","3","3","3","3"]],[["U","U","U","U","U","U"]],[["B","B","B","B","B","B"]]] 
BRICKS_Y = [5,7,9,11]

BRICKS_START_X_EVEN = 6
BRICKS_END_X_EVEN = 104
BRICK_XGAP = 10
NO_OF_POWERUP = 10
POWERUPS = ["E","S","M","F","T","G","O","P"]
PADDLE_LENGTH = 11
BLAST_BRICK_Y = [11,9]
BRICK_INIT_H = 5
BRICK_GAP = 4
NumberOfBricksRow = 2
NUMBEROFRAINBOW = 3
BRICK_FIN_H = (NumberOfBricksRow-1) * BRICK_GAP + 1 + BRICK_INIT_H
NUMBEROFUNBRICKS = 2
BULLET = ["^"]
UFOX = 5
decent = 4
Bomb = ["V"]
UFO =[[" "," "," "," "," ","_","_","_"," "," "," "," "," "],
[" ","_","_","_","/"," "," "," "," ","\\","_","_","_","_"],
["/"," "," "," ","'","~","~","~","'"," "," "," ","\\"],
["'","-","-","_","_","_","_","_","_","_","-","-","'"],
[" "," "," "," "," ","/","_","\\"," "," "," "," "," "]] 
HeightofUfo = len(UFO)
WidthofUfo = len(UFO[0])
UFOY = decent 

#      ___     
#  ___/   \___ 
# /   '---'   \
# '--_______--'
#      / \     

# EXPAND PADDLE = E   0
# SHRINK PADDLE = S   1
# BALL MULTIPLIER = M  2
# FAST BALL = F  3
# THRU BALL = T  4
# PADDLE GRAB = G  5
# fireball = O  6
# bullet = P 7




