import config
import random
from colorama import init, Fore, Back, Style
import numpy as np

class Map(object):

    height = int(config.rows) 
    width = int(config.columns)

    def __init__(self):
        self.start_index = 0
        self.matrix = np.array([[" " for i in range(self.width)] for j in range(self.height)])
        self.create_sky()
        self.create_ground()
        self.create_lwall()
        self.create_rwall()

    def render(self):
        for y in range(3, self.height):
            pr = []
            for x in range(self.start_index, self.start_index + config.columns):
                if y == 3:
                    pr.append(Fore.LIGHTCYAN_EX + Style.BRIGHT+(self.matrix[y][x] + Style.RESET_ALL))

                elif y == self.height - 1:
                    pr.append(Fore.LIGHTMAGENTA_EX + Style.BRIGHT+(self.matrix[y][x] + Style.RESET_ALL))
                elif self.matrix[y][x] == '#':
                    pr.append(Fore.LIGHTCYAN_EX  + self.matrix[y][x] + Style.RESET_ALL) 
                elif self.matrix[y][x] == '@':
                    pr.append(Fore.YELLOW + self.matrix[y][x] + Style.RESET_ALL) 
                elif self.matrix[y][x] == '1':
                    pr.append( Fore.LIGHTGREEN_EX + Back.LIGHTGREEN_EX + self.matrix[y][x] + Style.RESET_ALL)
                elif self.matrix[y][x] == '2':
                    pr.append(Fore.LIGHTMAGENTA_EX + Back.LIGHTMAGENTA_EX + self.matrix[y][x] + Style.RESET_ALL)
                elif self.matrix[y][x] == '3':
                    pr.append(Fore.RED + Back.RED + self.matrix[y][x] + Style.RESET_ALL)    
                elif self.matrix[y][x] == 'U':
                    pr.append(Fore.LIGHTCYAN_EX + Back.LIGHTCYAN_EX + self.matrix[y][x] + Style.RESET_ALL)
                elif self.matrix[y][x] == 'E':
                    pr.append(Fore.LIGHTRED_EX + Back.LIGHTRED_EX + self.matrix[y][x] + Style.RESET_ALL)
                elif self.matrix[y][x] == 'S':
                    pr.append(Fore.WHITE + Back.WHITE + self.matrix[y][x] + Style.RESET_ALL)
                elif self.matrix[y][x] == 'M':
                    pr.append(Fore.LIGHTBLACK_EX + Back.LIGHTBLACK_EX + self.matrix[y][x] + Style.RESET_ALL)
                elif self.matrix[y][x] == 'F':
                    pr.append(Fore.LIGHTYELLOW_EX + Back.LIGHTYELLOW_EX + self.matrix[y][x] + Style.RESET_ALL)
                elif self.matrix[y][x] == 'T':
                    pr.append(Fore.BLUE + Back.BLUE + self.matrix[y][x] + Style.RESET_ALL)
                elif self.matrix[y][x] == 'G':
                    pr.append(Fore.GREEN + Back.GREEN + self.matrix[y][x] + Style.RESET_ALL)
                elif self.matrix[y][x] == 'B':
                    pr.append(Fore.LIGHTBLACK_EX + Back.BLACK + self.matrix[y][x] + Style.RESET_ALL)
                elif self.matrix[y][x] == 'O':
                    pr.append(Fore.MAGENTA + Back.MAGENTA + self.matrix[y][x] + Style.RESET_ALL)
                else:
                    pr.append(self.matrix[y][x] + Style.RESET_ALL)
            print(''.join(pr))

    def create_ground(self):
        y = self.height - 1
        for x in range(self.width):
            self.matrix[y][x] = "T"


    def create_sky(self): 
        for x in range(self.width):
            self.matrix[3][x] = "X"

    def create_rwall(self):
        x = self.width - 1
        for y in range(self.height):
            self.matrix[y][x] = "|"
    
    def create_lwall(self):
        x = 0
        for y in range(self.height):
            self.matrix[y][x] = "|"
