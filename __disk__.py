"""
The disk class represents a disk in the towers of hanoi game.
Disks vary by their widths.
"""

class Disk:
	def __init__(self, width):
		""" Creates a disk object with width 'width.'  A disk with width 0 is an
		    "empty disk" that represents an empty space on the board."""
		self.width = width

	def __repr__(self):
		return str(self.width)

	def compact_str(self, num_disks, numbers):
		""" Compact representation, when there are > 5 disks """
		width = self.width
		width_mult = 0
		base = 0
		if num_disks <= 3:
			width_mult = 4
			base = num_disks * 2
			if numbers:
				base += 1
		elif num_disks <= 5:
			width_mult = 4
			base = num_disks * 2 - 8
			if numbers:
				base += 1
		else:
			width_mult = 2
			base = 2
			if numbers:
				base += 1
		s = "┌" + "-"*(base + width_mult*width - 2) + "┐\n"
		if numbers:
			half_base = (base + width_mult*width - 2 - 1) // 2
			s = "┌" + "-"*half_base + str(self.width) + "-"*half_base + "┐\n"
		s += "|" + " "*(base + width_mult*width - 2) + "|\n"
		s += "└" + "-"*(base + width_mult*width - 2) + "┘"
		return s

	def non_compact_str(self, num_disks, numbers):
		""" non-compact representation, when there are <= 5 disks """
		width = self.width
		width_mult = 0
		base = 0
		if num_disks <= 3:
			width_mult = 4
			base = num_disks * 2
			if numbers:
				base += 1
		elif num_disks <= 5:
			width_mult = 4
			base = num_disks * 2 - 8
			if numbers:
				base -= 1
		else:
			width_mult = 2
			base = 2
			if numbers:
				base += 1
		half_base = (base + width_mult*width - 2 - 1) // 2
		s =  "┌" + "-"*(base + width_mult*width - 2) + "┐\n"
		if numbers:
			s += "|" + " "*half_base + str(self.width) + " "*half_base + "|\n"
		else:
			s += "|" + " "*(base + width_mult*width - 2) + "|\n"
		s += "└" + "-"*(base + width_mult*width - 2) + "┘"
		return s

	def to_lines(self, num_disks, is_top, numbers):
		""" returns line-by-line string representation of the disk.
			always returns non-compact form if is_top == true.
			else returns compact/non-compact depending on the number
			of disks. If numbers==True, prints disk with its width
			in the center.  """
		comp = self.compact_str(num_disks, numbers).split("\n")
		non_comp = self.non_compact_str(num_disks, numbers).split("\n")
		return non_comp if is_top or num_disks <= 5 else comp

class EmptyDisk(Disk):
	def __init__(self, width=0):
		Disk.__init__(self, width)