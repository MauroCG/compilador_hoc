# coding -utf-8

from hoclex import HOCLexer
from hocparser import HOCParser
import argparse


def Menu():
		print("Digite una opcion: \n")
		print("1. Analísis Léxico")
		print("2. Analísis Sintáctico")
		print("3. Árbol de sintaxis abstracto (AST) \n")
		op = input("Digite su elección -> ")
		op = int(op)
		assert(op <= 3 and op >= 1)
		return op


class Facade(object):
	def __init__(self, codehoc):
		self.lex = HOCLexer()
		self.parser = HOCParser()
		self.codehoc = codehoc

	def lexico(self):
		for tok in self.lex.tokenize(self.codehoc):
			print(tok)

	def sintactico(self):
		self.parser.parse(self.lex.tokenize(self.codehoc))

	def ast(self):
		ast = self.parser.parse(self.lex.tokenize(self.codehoc))
		ast.pprint()


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--lex", help='Muestra el analísis léxico del Código')
	parser.add_argument("codigo", help="Código a compilar, con extensión .hoc")
	args = parser.parse_args()
	codehoc = args.codigo
	text = open(codehoc).read()
	facade = Facade(text)
	if args.lex is not None:
		facade.lexico()
		return
	op = Menu()
	if op == 1:
		facade.lexico()
	elif op == 2:
		facade.sintactico()
	elif op == 3:
		facade.ast()




if __name__ == "__main__":
	main()


