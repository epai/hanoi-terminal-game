""" The AI class encapsulates logic behind a "Machine player"
	that uses recursion to solve Hanoi puzzles of any disk amount.
	Algorithm created by Eric Pai.  """

import curses

class AI:
	""" suggestions:
		- menu
	"""

	def __init__(self, main, num_disks):
		self.m = main
		self.num = num_disks
		self.moves = []

	def move_all(self, n, curr, dest, extra):
		""" moves n disks from the 'curr' pole to 'dest' pole,
			using the 'extra' pole for 'temporary storage.'
			Assume all disks are on curr pole, no disks are on dest pole,
			and no disks are on extra pole (as in original game state). """
		if n == 1:
			self.moves.append((curr, dest))
		else:
			self.move_all(n-1, curr, extra, dest)
			self.moves.append((curr, dest))
			self.move_all(n-1, extra, dest, curr)


