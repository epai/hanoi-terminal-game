""" The game class encapsulates all internal game logic. """

"""
             ||                         ||                         ||
             ||                         ||                         ||
             ||                         ||                         ||
        ┌----------┐                    ||       by Eric Pai       ||
        |          |                    ||                         ||
        └----------┘      HANOI         ||                         ||
      ┌--------------┐                  ||            :)           ||
      |              |                  ||                         ||
      └--------------┘                  ||                         ||
    ┌------------------┐             ┌------┐                      ||
    |                  |             |      |                      ||
    └------------------┘             └------┘                      ||

"""

import os
import sys
from __disk__ import *

class Game:
	# treat each pole as a stack data structure

	def __init__(self, width, height, disks=5, poles=3):
		""" Takes in four parameters:
				- number of disks
				- number of poles
				- width of terminal
				- height of terminal
			...and initializes and sets up the game logic."""
		self.stack = [[] for p in range(poles)]
		self.stack[0] = [Disk(disks - i) for i in range(disks)]
		for i in range(1, poles):
			self.stack[i] = [EmptyDisk() for _ in range(disks)]
		self.num_disks = disks
		self.num_poles = poles
		self.width = width
		self.height = height
		self.curr_pole = 0
		self.numbers = False
		#self.curr_disk = None

	#################
	# GAME MECANICS #
	#################
	def pop(self, pole):
		""" Removes the top disk from the 'pole' """
		for i in range(self.num_disks + 1):
			if i == self.num_disks or type(self.stack[pole][i]) is EmptyDisk:
				break
		if i > 0:
			top_disk = self.stack[pole][i - 1]
			self.stack[pole][i - 1] = EmptyDisk()
			return top_disk
		return None

	def can_push(self, disk, pole):
		""" Determines whether it's possible to push 'disk' onto 'pole' """
		for i in range(self.num_disks):
			if type(self.stack[pole][i]) is EmptyDisk:
				break
		if i == 0 or disk.width < self.stack[pole][i - 1].width:
			return True
		return False

	def push(self, disk, pole):
		""" Pushes 'disk' at the top of the pole, if possible """
		for i in range(self.num_disks):
			if type(self.stack[pole][i]) is EmptyDisk:
				break
		self.stack[pole][i] = disk

	@property
	def win(self):
		for i in range(self.num_disks):
			if self.stack[self.num_poles - 1][i].width != self.num_disks - i:
				return False
		return True

	####################
	# GUI & UX METHODS #
	####################
	def print_stack(self):
		""" Returns the string GUI representation of the stack """
		width_size = 23 if self.numbers else 24
		s = ""
		poles = [[] for _ in range(self.num_poles)]
		for pole in range(self.num_poles):
			pole_lines = []
			pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
			pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
			if self.num_disks <= 5:
				for _ in range(5 - self.num_disks):
					pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
					pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
					pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
			else:
				for _ in range(11 - self.num_disks):
					pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
					pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
					pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
			for i in range(self.num_disks):
				disk = self.stack[pole][self.num_disks - 1 - i]
				if type(disk) is EmptyDisk:
					pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
					pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
					pole_lines.append(("|" + " "*(self.numbers) + "|").center(width_size))
				else:
					s = disk.to_lines(self.num_disks, False, self.numbers)
					pole_lines.append(s[0].center(width_size))
					pole_lines.append(s[1].center(width_size))
					pole_lines.append(s[2].center(width_size))

			poles[pole] = pole_lines
		return poles

	def get_highlighted(self):
		height = 13
		width = 23 if self.numbers else 24
		lines = []
		lines.append("┌" + "-"*(width) + "┐")
		for i in range(height):
			line = "|" + " "*(width) + "|"
			lines.append(line)
		return lines

	def move_highlighted(self, direction):
		""" Moves the 'highlighted' box one pole left or right.
				param direction:  -1 = left, +1 = right"""
		if direction == -1:
			if self.curr_pole - 1 >= 0:
				self.curr_pole -= 1
			else:
				# cannot go past left-most pole
				pass
		elif direction == 1:
			if self.curr_pole + 1 <= self.num_poles - 1:
				self.curr_pole += 1
			else:
				# cannot go past right-most pole
				pass
		else:
			# invalid direction
			pass

	def __str__(self):
		""" Returns the string GUI representation of thes tack, for ease of
			debugging. """
		s = ""
		for line in g.print_stack():
			s += line
		return s



