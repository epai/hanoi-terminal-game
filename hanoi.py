"""
Welcome to the towers of hanoi!
Thanks for checking out the code.

All code was made by Eric Pai.  Made in 2014.

the __disk__.py file encapsulates the internal representations of disks.
	it also encapsulates how disks are represented in string form (GUI)
the __game__.py file encapsulates the main game logic and many GUI functions
the __Main__.py file takes care of actually running the game, and also takes
	care of animation/high-level GUI features (such as menus)
and this file (hanoi.py) combines all elements of the other classes to actually
	run the game.

A lot of code in the __Main__.py file is adopted from tetris.py, another terminal
	game I made previously.

Enjoy!
"""

"""suggestions:
	-add color
	-add music
"""

from __Main__ import *

m = Main()
try:
	m.do_welcome()
	m.game_loop()
except ZeroDivisionError as e:
    pass
except KeyboardInterrupt as e:
    pass
except Exception as e:
    raise e
finally:
    m.do_finish()
