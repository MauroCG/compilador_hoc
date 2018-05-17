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
	parser = argparse.ArgumentParser(description="Ayuda en las etapas de compilación, permitiendo mostrar cada una por separado")
	group = parser.add_mutually_exclusive_group()

	group.add_argument("-l", "--lex", help='Muestra el analísis léxico del Código pasado',
	action='store_true')
	group.add_argument("-p", "--parse", help='Muestra el analísis sintáctico del Código pasado',
	action='store_true')
	group.add_argument("-a", "--ast", help='Muestra el AST del código pasado',
	action='store_true')

	parser.add_argument("codigo", help="Código a compilar, con extensión .hoc")
	args = parser.parse_args()

	codehoc = args.codigo
	text = open(codehoc).read()
	facade = Facade(text)

	if args.lex:
		facade.lexico()
		return

	if args.parse:
		facade.sintactico()
		return

	if args.ast:
		facade.ast()
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