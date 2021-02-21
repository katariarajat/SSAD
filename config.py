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
BRICKS_START_X = 5
BRICKS_END_X = 104
NO_OF_POWERUP = 100
POWERUPS = ["E","S","M","F","T","G"]
PADDLE_LENGTH = 11
BLAST_BRICK_Y = [11,9]
# EXPAND PADDLE = E   0
# SHRINK PADDLE = S   1
# BALL MULTIPLIER = M  2
# FAST BALL = F  3
# THRU BALL = T  4
# PADDLE GRAB = G  5



