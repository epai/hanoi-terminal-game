""" The Main class encapsulates all internal game mechanics,
    and GUI representations """

import curses
from __game__ import *
from __welcome__ import *
from hanoi_ai import *

class Main:

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.stdscr.nodelay(False)
        curses.curs_set(0)
        self.version = 1.0

        self.g = None
        self.curr_disk = None
        self.do_shake = False
        self.restart = False
        self.tutorial = False
        self.ai_paused = False

    #######################
    # Main Game Mechanics #
    #######################
    def do_welcome(self):
        """ Handles welcome screen """
        self.stdscr.nodelay(True)
        self.stdscr.addstr(0, 0, welcome_message[0])
        start = False
        blink_counter = 1
        blink = True
        animate_counter = 0
        refresh_counter = 10
        while (not start):
            c = self.stdscr.getch()
            for i in range(10000):
                c = self.stdscr.getch()
                if c != -1:
                    start = True
                    break
            if refresh_counter == 10:
                refresh_counter = 1
                if animate_counter == len(welcome_message):
                    animate_counter = 0
                self.stdscr.addstr(0, 10, welcome_message[animate_counter])
                animate_counter += 1
                if blink:
                    self.stdscr.addstr(18, 22, "                                  ")
                else:
                    self.stdscr.addstr(18, 25, "   Press ANY key to start!     ")

                blink = not blink
                blink_counter = 0
            refresh_counter += 1
            self.stdscr.addstr(23, 0, "v{0} Eric Pai ©2014".format(self.version))
            curses.delay_output(5)
            blink_counter += 1
            self.stdscr.refresh()
        self.stdscr.nodelay(False)

    def do_setup(self):
        objective = \
        """
           Objctive:  Move disks from first pole to last
                      (stacked smallest on top) one disk at a time.

           Controls:  'up' key - lift a disk
                      'down' key - drop a disk
                      'left' key - switch to left pole
                      'right' key - switch to right pole

              ||                         ||                         ||
              ||                         ||                         ||
              ||                         ||                         ||
    ┌--------------------┐               ||                         ||
    |     ┌--------┐     |               ||                         ||
    |     |        |     |               ||                         ||
    |   ┌------------┐   |--------------------------------------->  ||
    |   |            |   |               ||                         ||
    | ┌----------------┐ |               ||                         ||
    | |                | |               ||                         ||
   ┌|--------------------|--------------------------------------------------┐
   └------------------------------------------------------------------------┘"""
        curses.nocbreak()
        curses.echo()
        curses.curs_set(2)
        self.stdscr.clear()
        self.stdscr.addstr(2, 0, objective)
        self.stdscr.addstr(2, 0, "-"*75)
        self.stdscr.addstr(0, 6,     "toggle machine player (ai)? (type y/n, press enter)  ")
        c = self.stdscr.getch()
        while c not in (ord('y'), ord('n')):
            self.stdscr.clear()
            self.stdscr.addstr(2, 0, objective)
            self.stdscr.addstr(2, 0, "-"*75)
            self.stdscr.addstr(0, 6, "toggle machine player (ai)? (type y/n, press enter)  ")
            self.stdscr.refresh()
            c = self.stdscr.getch()
        self.ai = True if c == ord('y') else False
        self.stdscr.clear()
        self.stdscr.addstr(2, 0, objective)
        self.stdscr.addstr(2, 0, "-"*75)
        self.stdscr.addstr(0, 6,     "       How many disks? (enter a number from 2 to 9)  ")
        self.stdscr.refresh()
        c = self.stdscr.getch()
        while c not in [ord(str(i)) for i in range(2, 10)]:
            self.stdscr.clear()
            self.stdscr.addstr(2, 0, objective)
            self.stdscr.addstr(2, 0, "-"*75)
            self.stdscr.addstr(0, 6,     "       How many disks? (enter a number from 2 to 9)  ")
            self.stdscr.refresh()
            c = self.stdscr.getch()
        for j in range(2, 10):
            if c == ord(str(j)):
                break
        width, height = \
                [int(x) for x in os.popen('stty size', 'r').read().split()]
        self.g = Game(height, width, j)
        self.num_moves = 0
        curses.cbreak()
        curses.curs_set(0)
        curses.noecho()

    def game_loop(self):
        """ Main game loop. All the juicy __game__ logic is used here. """
        c = ""
        while True:
            self.do_restart()
            if self.ai:
                ai = AI(self, self.g.num_disks)
                ai.move_all(ai.num, 0, 2, 1)
                ai.i = 0
                while ai.i < len(ai.moves):
                    self.ai_stepper(ai) if self.ai_paused else self.ai_auto(ai)
                    if self.restart:
                        break
                if self.restart:
                    self.stdscr.nodelay(False)
                    continue
                self.refresh_screen()
                self.do_win()
                self.stdscr.nodelay(False)
                continue
            while True:
                self.refresh_screen()
                self.handle_events()
                if self.g.win:
                    self.refresh_screen()
                    self.do_win()
                if self.restart:
                    break

    def handle_events(self):
        c = self.stdscr.getch()
        if c == curses.KEY_LEFT:
            self.g.move_highlighted(-1)
        elif c == curses.KEY_RIGHT:
            self.g.move_highlighted(1)
        elif c == curses.KEY_UP:
            if self.curr_disk is None:
                disk = self.g.pop(self.g.curr_pole)
                if disk is not None:
                    self.curr_disk = disk
        elif c == curses.KEY_DOWN:
            if self.curr_disk is None:
                pass
            elif not self.g.can_push(self.curr_disk, self.g.curr_pole):
                self.do_shake = True
            else:
                self.g.push(self.curr_disk, self.g.curr_pole)
                self.curr_disk = None
                self.num_moves += 1
        elif c == ord('q'):
            self.do_quit()
        # elif c == ord('p'):
        #   self.do_pause()
        elif c == ord('m'):
            self.do_menu()

    def do_restart(self):
        self.g = None
        self.curr_disk = None
        self.do_shake = False
        self.restart = False
        self.wait_time = 6
        self.direction = 0
        self.ai_paused = True
        self.do_setup()

    #####################
    # Graphics Handling #
    #####################
    def refresh_screen(self):
        """ All-encompassing method that handles graphics/animation """
        self.stdscr.clear()
        c = 5
        # prints highlighted box
        for line in self.g.get_highlighted():
            self.stdscr.addstr(c, self.g.curr_pole * 27, line)
            c += 1
        # prints 'table'
        self.stdscr.addstr(19, 1, "┌" + "-"*(self.g.width - 4) + "┐")
        self.stdscr.addstr(20, 1, "└" + "-"*(self.g.width - 4) + "┘")
        self.stdscr.addstr(21, 0, " "*4 + "|" + " "*(self.g.width - 10) + "|" + " "*4)
        self.stdscr.addstr(22, 0, " "*4 + "|" + " "*(self.g.width - 10) + "|" + " "*4)
        # prints 'menu' things
        if self.num_moves < 1 and not self.ai:
            self.stdscr.addstr(21, 5, "Press 'm' for menu/pause, 'q' to quit,".center(self.g.width - 10))
        # prints disks and poles
        self.do_disks_and_poles()
        # prints top disk
        if self.curr_disk is not None:
            disk = self.curr_disk.to_lines(self.g.num_disks, True, self.g.numbers)
            for i in range(len(disk)):
                self.stdscr.addstr(i+2, self.g.curr_pole * 27 + 1, disk[i].center(24))
        # if do_shake = True, do shake
        if self.do_shake:
            self.do_shake_method()
        # print num_moves
        self.stdscr.addstr(1, 50, "Number moves = {0}".format(self.num_moves))
        # finally.. refresh the screen
        self.stdscr.refresh()

    def do_disks_and_poles(self):
        """ Prints current arrangement of disks and poles """
        i = 4
        c = 8
        r = 1
        lines = self.g.print_stack()
        if self.g.num_disks <= 5:
            for pole in lines:
                for disk in pole:
                    if (i+1)%3 != 0:
                        self.stdscr.addstr(c, r, disk)
                        c += 1
                    i += 1
                r += 27
                c = 8
                i = 4
        else:
            for pole in lines:
                for disk in pole:
                    if i%3 == 0:
                        self.stdscr.addstr(c, r, disk)
                        c += 1
                    i += 1
                r += 27
                c = 8
                i = 4

    def do_shake_method(self):
        """ 'Shakes' the top piece. Provides visual feedback when the
             user makes an error. """
        if self.curr_disk is not None:
            disk = self.curr_disk.to_lines(self.g.num_disks, True, self.g.numbers)
        for i in range(len(disk)):
            self.stdscr.addstr(i+2, self.g.curr_pole * 27, disk[i].center(24))
        self.stdscr.refresh()
        curses.delay_output(25)
        for i in range(len(disk)):
            self.stdscr.addstr(i+2, self.g.curr_pole * 27 + 2, disk[i].center(24))
        self.stdscr.refresh()
        curses.delay_output(25)
        for i in range(len(disk)):
            self.stdscr.addstr(i+2, self.g.curr_pole * 27 + 1, disk[i].center(24))
        self.do_shake = False

    def do_quit(self):
        """ Handles the pop-up window when the user wants to quit """
        self.stdscr.addstr(10, 24, "┌--------------------------------┐")
        self.stdscr.addstr(11, 24, "| Are you sure you want to quit? |")
        self.stdscr.addstr(12, 24, "|                                |")
        self.stdscr.addstr(13, 24, "|    'y' for yes, 'n' for no     |")
        self.stdscr.addstr(14, 24, "└--------------------------------┘")
        self.stdscr.refresh()
        c = self.stdscr.getch()
        while c not in (ord('y'), ord('n')):
            c = self.stdscr.getch()
        if c == ord('y'):
            raise ZeroDivisionError

    def do_menu(self):
        def print_menu1():
            self.stdscr.addstr(4, 24,  "┌--------------------------------┐")
            self.stdscr.addstr(5, 24,  "|          Game Paused           |")
            self.stdscr.addstr(6, 24,  "|                                |")
            self.stdscr.addstr(7, 24,  "| Controls:     ^ Lift disk      |")
            self.stdscr.addstr(8, 24,  "|               |                |")
            self.stdscr.addstr(9, 24,  "| Move left <--   --> Move right |")
            self.stdscr.addstr(10, 24, "|               |                |")
            self.stdscr.addstr(11, 24, "|               V Drop disk      |")
            self.stdscr.addstr(12, 24, "|                                |")
            self.stdscr.addstr(13, 24, "| Type 'm' to resume,            |")
            self.stdscr.addstr(14, 24, "|      'q' to quit               |")
            self.stdscr.addstr(15, 24, "|      'r' to restart            |")
            self.stdscr.addstr(16, 24, "|      'n' to turn off/on num's  |")
            self.stdscr.addstr(17, 24, "└--------------------------------┘")
            self.stdscr.refresh()
        def print_menu2():
            self.stdscr.addstr(4, 24,  "┌--------------------------------┐")
            self.stdscr.addstr(5, 24,  "|          Game Paused           |")
            self.stdscr.addstr(6, 24,  "|                                |")
            self.stdscr.addstr(7, 24,  "| Controls:     ^ Incr speed     |")
            self.stdscr.addstr(8, 24,  "|               |                |")
            self.stdscr.addstr(9, 24,  "|                                |")
            self.stdscr.addstr(10, 24, "|               |                |")
            self.stdscr.addstr(11, 24, "|               V Decr speed     |")
            self.stdscr.addstr(12, 24, "|                                |")
            self.stdscr.addstr(13, 24, "| Type 'm' to resume,            |")
            self.stdscr.addstr(14, 24, "|      'q' to quit               |")
            self.stdscr.addstr(15, 24, "|      'r' to restart            |")
            self.stdscr.addstr(16, 24, "|      'n' to turn off/on num's  |")
            self.stdscr.addstr(17, 24, "└--------------------------------┘")
            self.stdscr.refresh()
        def print_menu3():
            self.stdscr.addstr(4, 24,  "┌--------------------------------┐")
            self.stdscr.addstr(5, 24,  "|          Game Paused           |")
            self.stdscr.addstr(6, 24,  "|                                |")
            self.stdscr.addstr(7, 24,  "| Controls:     ^ Incr speed     |")
            self.stdscr.addstr(8, 24,  "|               |                |")
            self.stdscr.addstr(9, 24,  "| back one  <--   -->   frwd one |")
            self.stdscr.addstr(10, 24, "|     step      |           step |")
            self.stdscr.addstr(11, 24, "|               V Decr speed     |")
            self.stdscr.addstr(12, 24, "|                                |")
            self.stdscr.addstr(13, 24, "| Type 'm' to resume,            |")
            self.stdscr.addstr(14, 24, "|      'q' to quit               |")
            self.stdscr.addstr(15, 24, "|      'r' to restart            |")
            self.stdscr.addstr(16, 24, "|      'n' to turn off/on num's  |")
            self.stdscr.addstr(17, 24, "└--------------------------------┘")
            self.stdscr.refresh()
        if self.ai:
            if self.ai_paused:
                print_menu3()
            else:
                print_menu2()
        else:
            print_menu1()
        while True:
            c = self.stdscr.getch()
            while c not in (ord('q'), ord('r'), ord('m'), ord('n'), ord('h')):
                c = self.stdscr.getch()
            if c == ord('q'):
                self.do_quit()
                print_menu()
            if c == ord('r'):
                self.stdscr.addstr(10, 21, "┌-----------------------------------┐")
                self.stdscr.addstr(11, 21, "| Are you sure you want to restart? |")
                self.stdscr.addstr(12, 21, "|                                   |")
                self.stdscr.addstr(13, 21, "|      'y' for yes, 'n' for no      |")
                self.stdscr.addstr(14, 21, "└-----------------------------------┘")
                self.stdscr.refresh()
                c = self.stdscr.getch()
                while c not in (ord('y'), ord('n')):
                    c = self.stdscr.getch()
                if c == ord('y'):
                    self.restart = True
                    break
                if c == ord('n'):
                    self.refresh_screen()
                    if self.ai:
                        if self.ai_paused:
                            print_menu3()
                        else:
                            print_menu2()
                    else:
                        print_menu1()
                    self.stdscr.refresh()
                    continue
            if c == ord('n'):
                self.g.numbers = not self.g.numbers
                self.refresh_screen()
                if self.ai:
                    if self.ai_paused:
                        print_menu3()
                    else:
                        print_menu2()
                else:
                    print_menu1()
                self.stdscr.refresh()
            if c == ord('m'):
                break

    def do_win(self):
        self.stdscr.addstr(10, 24, "┌--------------------------------┐")
        self.stdscr.addstr(11, 24, "|                                |")
        self.stdscr.addstr(12, 24, "|            You win!            |")
        self.stdscr.addstr(13, 24, "|                                |")
        self.stdscr.addstr(14, 24, "└--------------------------------┘")
        self.stdscr.refresh()
        curses.delay_output(1500)
        s = ("Moves made: {0}".format(self.num_moves)).center(32)
        self.stdscr.addstr(12, 24, "|" + s +"|")
        self.stdscr.refresh()
        curses.delay_output(1500)
        self.stdscr.addstr(9, 24,  "┌--------------------------------┐")
        self.stdscr.addstr(10, 24, "|           Play again?          |")
        self.stdscr.addstr(11, 24, "|                                |")
        self.stdscr.addstr(13, 24, "|                                |")
        self.stdscr.addstr(14, 24, "|     'y' for yes, 'n' for no    |")
        self.stdscr.addstr(15, 24, "└--------------------------------┘")
        self.stdscr.refresh()
        c = self.stdscr.getch()
        while c not in (ord('y'), ord('n')):
            c = self.stdscr.getch()
        if c == ord('y'):
            self.restart = True
        if not self.restart:
            raise ZeroDivisionError

    def do_finish(self):
        """ Reverts original terminal settings. This method is called when
             the application is closed. """
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()

    #####################
    # AI helper methods #
    #####################

    # wait_time = 6  see self.restart() for initialization details

    def ai_refresh(self):
        self.refresh_screen()
        self.print_speed()
        self.print_direction()
        if not self.ai_paused:
            self.stdscr.addstr(21, 5, "   Press 'm' for menu, 'p' to pause, 'up'/'down' to incr/decr speed")
        else:
            self.stdscr.addstr(21, 5, "       Press 'left' to go back one step, and 'right' to go forward")
            self.stdscr.addstr(22, 5, "             'p' to unpause/continue, and 'm' to access the menu. ")
        self.stdscr.refresh()
        i = 0
        while i < self.wait_time:
            if not self.ai_paused:
                self.handle_inputs()
            curses.delay_output(10)
            i += 1

    def move_disk(self, pole1, pole2):
        """ move top disk from pole1 to pole2, and animate the movement.
            assume you can remove a disk from pole1 and push it onto pole2. """
        # move highlighted box to pole1
        while pole1 > self.g.curr_pole:
            self.g.move_highlighted(1)
            self.ai_refresh()
        while pole1 < self.g.curr_pole:
            self.g.move_highlighted(-1)
            self.ai_refresh()
        # remove top disk from pole1
        disk = self.g.pop(self.g.curr_pole)
        self.curr_disk = disk
        self.ai_refresh()
        # move highlighted box to pole2
        while pole2 > self.g.curr_pole:
            self.g.move_highlighted(1)
            self.ai_refresh()
        while pole2 < self.g.curr_pole:
            self.g.move_highlighted(-1)
            self.ai_refresh()
        # add disk to top of pole2
        self.g.push(self.curr_disk, self.g.curr_pole)
        self.curr_disk = None
        self.ai_refresh()

    def print_speed(self):
        wait = self.wait_time - 1
        speed = "[" + "*"*(10 - wait) + " "*(wait) + "]" + " speed: {0} ".format(10 - wait)
        self.stdscr.addstr(0, 0, speed)

    def incr_speed(self):
        if self.wait_time > 1:
            self.wait_time -= 1

    def decr_speed(self):
        if self.wait_time < 10:
            self.wait_time += 1

    def handle_inputs(self):
        c = self.stdscr.getch()
        if c == curses.KEY_UP:
            self.incr_speed()
        elif c == curses.KEY_DOWN:
            self.decr_speed()
        elif c == ord('p'):
            self.ai_paused = True
        elif c == ord('m'):
            self.do_menu()

    def print_direction(self):
        if self.direction == 0:
            self.stdscr.addstr(0, 28, "  ")
        if self.direction == 1:
            self.stdscr.addstr(0, 28, ">>")
        if self.direction == -1:
            self.stdscr.addstr(0, 28, "<<")

    def ai_auto(self, ai):
        self.stdscr.nodelay(True)
        self.ai_refresh()
        self.direction = 0
        self.handle_inputs()
        if not self.restart:
            self.move_disk(ai.moves[ai.i][0], ai.moves[ai.i][1])
        self.num_moves += 1
        ai.i += 1

    def ai_stepper(self, ai):
        self.stdscr.nodelay(False)
        self.ai_refresh()
        self.stdscr.addstr(0, 26, "PAUSED")
        self.stdscr.refresh()
        c = self.stdscr.getch()
        while c not in (curses.KEY_LEFT, curses.KEY_RIGHT, ord('p'),
                        curses.KEY_UP, curses.KEY_DOWN, ord('m')):
            c = self.stdscr.getch()
        if c == curses.KEY_LEFT:
            self.direction = -1
            if ai.i > 0:
                ai.i -= 1
                self.move_disk(ai.moves[ai.i][1], ai.moves[ai.i][0])
                self.num_moves -= 1
        elif c == curses.KEY_RIGHT:
            self.direction = 1
            if ai.i < len(ai.moves):
                self.move_disk(ai.moves[ai.i][0], ai.moves[ai.i][1])
                self.num_moves += 1
                ai.i += 1
        elif c == curses.KEY_UP:
            self.incr_speed()
        elif c == curses.KEY_DOWN:
            self.decr_speed()
        elif c == ord('p'):
            self.ai_paused = False
        elif c == ord('m'):
            self.do_menu()
        self.refresh_screen()
        self.print_speed()
        self.stdscr.refresh()


