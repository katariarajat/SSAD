# from getch import KBHit
# from global_var import mando, dragon
# from global_funct import remove_shield, allow_shield, move_board_back, check_speedup_time
# import global_var
# import global_funct
# import config
# from time import time
# import objects

# kb = KBHit()

# def movedin():
#     # moves the player
#     char = kb.getinput()

#     if char == 'd':
#         if mando.xget() <= global_var.mp.start_index + config.columns - 4 - mando.get_width() and mando.xget() <= 1090:
#             mando.xset(1)

#     if char == 'a':
#         if mando.xget() > global_var.mp.start_index + 4:
#             mando.xset(-1)

#     if char == 'w':
#         if mando.yget() >= 5:
#             mando.yset(-1)
#             mando.set_air_pos(mando.yget())
#             mando.set_air_time(time())

#     if char == ' ' and mando.get_shield_allow() == 1:
#         mando.set_shield_allow(0)
#         mando.set_shield_time(time())
#         mando.set_shield(1)

#     if char == 'e':
#         bullet = objects.Bullet(config.bullet, mando.xget() + 4, mando.yget()+1)
#         bullet.render()
#         global_var.bullets.append(bullet)

#     if char == 'q':
#         message = "Y U Quit :'("
#         global_funct.display_ending(message)
#         quit()


"""Defining input class."""
import sys
import termios
import tty
import signal

class Get:
    """Class to get input."""

    def __call__(self):
        """Defining __call__."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class AlarmException(Exception):
    """Handling alarm exception."""
    pass


def alarmHandler(signum, frame):
    """Handling timeouts."""
    raise AlarmException


def input_to(getch, timeout=0.1):
    """Taking input from user."""
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        text = getch()
        signal.alarm(0)
        return text
    except AlarmException:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return None