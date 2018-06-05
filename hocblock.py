# hocblock.py
# -*- coding: utf-8 -*-

# Clases utilizadas para guardar los bloques de código correspondientes

class BasicBlock(object):
	def __init__(self):
		self._block = []
		self.next_block = None

	def append(self, block):
		block = [block]
		self._block.append(block)

	def __repr__(self):
		if self._block:
			for inst in self._block:
				print(*inst)

		if self.next_block:
				print(self.next_block)

		return ' '



class IfBlock(BasicBlock):
	def __init__(self):
		super().__init__()
		self.test = None
		self.if_branch = None
		self.else_branch = None
		self.next_block = None

	def __repr__(self):
		if self.if_branch:
			print(self.if_branch)

		if self.else_branch:
			print(self.else_branch)

		if self.next_block:
			print(self.next_block)

		return ' '


class WhileBlock(BasicBlock):
	def __init__(self):
		super().__init__()
		self.test = None
		self.body = None
		self.next_block = None

	def __repr__(self):
		if self.body:
			print(self.body)

		if self.next_block:
			print(self.next_block)

		return ' '



# Clase para imprimir el contenido de los bloques

class PrintBlocks:
	def visit(self, start):
		print(start)