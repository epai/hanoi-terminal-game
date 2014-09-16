hanoi-terminal-game
===================

Towers of Hanoi game -- runs in the terminal, implemented in Python3 using the ncurses programming module.

***IMPORTANT:  PYTHON3 MUST BE INSTALLED TO PLAY***

to run, type:     
python3 hanoi.py      
in the terminal.


Objctive:  
Move disks from first pole to last
(stacked smallest on top) one disk at a time.
           
Controls:  
'up' key - lift a disk
'down' key - drop a disk
'left' key - switch to left pole
'right' key - switch to right pole


On Startup:
"toggle machine player" -- option to use AI.  To play normally, type "n".
"How many disks? (enter a number from 2 to 9)" -- specifies how many disks to use in the tower.
   
   
Keyboard shortcuts:

In ai mode:
'p' - pause/unpause
'm' - menu (includes instructions if you ever get lost)
'q' - to quit
'n' - toggle on/off number mode (to better see disk width)
'r' - to restart game (brings back to startup menu)
'up arrow' - increases animation speed
'down arrow' - decreases animation speed
'right arrow' - advances auto-solve one step forward
'left arrow' - moves one auto-solve step backwards
  
In regular mode:
'p' - pause
'n' - toggles on/off number mode (to better see disk width)
'r' - restart game (brings back to startup menu)
'q' - quit
'up arrow' - lift a disk
'down arrow' - drop a disk
'left arrow' - move left one pole
'right arrow' - move right one pole

credits:  Programmed and Designed by Eric Pai.  2013
