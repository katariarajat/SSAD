# Jetpack Joyride
### By Rajat Kumar - 2019101020

## Overview

An arcade game in Python3 (terminal-based), inspired from the old classic brick breaker.The objective of the game is to break all the bricks as fast as possible and beat the highest score! You lose a life when the ball touches the ground below the paddle. Concepts of object oriented programming is used to make the game

Rules of the Game
-------------------

> - You can control paddle using 'a' and 'd' key. 'a will take it to left and 'd' to right 
> - Once the ball touched the ground game resets and one life is lost. In case of multiple balls life will not be lost untill final ball touches ground 
> - You have 5 lives for your paddle, getting killed 5 times will result in a **GAME OVER**.
> - Destroying each bricks adds 1 points to the score.
> - The game run for the time untill your all life are lost.
> - You can exist a game anytime by pressing 'q' key when the game is running.
> - To release the ball from paddle press 'r' key continously


------------------------

Description of Classes Created
--------------------------------------------
#### Board:
The board class creates a 38*110 board for gameplay, with boundaries, walls and empty spaces. It also comprises of a print_board function to take a print of the board.

#### Object:
The Object class is the base class based on which all other entities of the game are inherited.

#### paddle:
The paddle class has all the variables and functionality of paddle, this includes the generation, movement, lives and powerups. It is inherited from Object class and has additional functionality. It also represents polymorphism as the render() function has been changed.

#### ball:
The ball class is inherited from the Object class and has functionality to move and collide with bricks, paddle and walls . It also has additional private variables such as strength etc.

#### bricks:
Inherited from Object class,it has funcitionality to change strength, color etc. It also contain function to release power.

#### powerups:
Inherited from Object class, it has functions to check and manipulate powerups gained by the paddle.

__________________

Concepts used
--------------------------------------------

#### Inheritance:

Inheritance allows us to define a class that inherits all the methods and properties from another class. 
A base class `Object` has been declared from which multiple elements are inherited.

```
class Object():
    
    def __init__(self, character, x, y):
        self._posx = x
        self._posy = y
        self._width = len(character[0])
        self._height = len(character)
        self._shape = character
```

#### Polymorphism

Polymorphism allows us to define methods in the child class with the same name as defined in their parent class. 
eg. 

```python
class Object():
    ...
    def xset(self, x):
        self._posx += x
```
```python

class paddle(Object):
    def xset(self, x):
        self._posx += x
        if self._posx > config.columns - 2:
            self._posx = config.columns - 2
        elif self._posx < 2:
            self._posx = 2
    
```

#### Encapsulation

The idea of wrapping data and the methods that work on data within one unit. Prevents accidental modification of data.
Implemented many classes and objects for the same.

```python
    def ball(Object):
```
#### Abstraction

Abstraction means hiding the complexity and only showing the essential features of the object.

```python

def ball(Object):
    ...
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
```
.move() is an abstraction

How To Play:
------------------
>- Run `pip3 -r install requirements.txt`
>- Run the following code to start the game.
```
python3 main.py
```
>- a, d' use these controls for  left, and right.
>- use 'r' to release ball. 
>- press 'q' to quit.

___________________

Reqiurements:
--------------------
- Python3

For mac:
```
brew cask update
sudo brew cask install python3
```
For Linux:
```
sudo apt-get update
sudo apt-get install python3
```

___________________

## Bricks description using colors:
---------------------
# LIGHTGREEN:
    Strength = 1
    character = 1
# LIGHTMAGENTA
    Strength = 2
    character = 2
# RED
    Strength = 3
    character = 3
# LIGHTCYAN
    Strength = Unbreakable 
    character = U
# LIGHTBLACK
    Strength = Blast 
    character = B
    Clears all 9 bricks nearby

___________________

## Power description using colors
---------------------
 
# LIGHTRED
    Power = Expand paddle
# WHITE
    Power = Shrink paddle
# LIGHTBLACK
    Power = Multiply ball(not more than 4)
# LIGHTYELLOW
    Power = Increase speed of Ball 
# BLUE
    Power = Ball passes thru bricks
# GREEN
    Power = Grab Ball

# BONUS IS IMPLEMENTED
# Time duration of power is 10 seconds 


